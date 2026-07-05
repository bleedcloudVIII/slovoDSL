import numpy as np

from netopt.enums import LayerType


class BNFolding:
    def __init__(self, structure: list, weights: dict):
        self.structure = structure
        self.weights = weights

    def _fold(self, conv_name: str, bn_name: str) -> dict:
        conv_w = self.weights[conv_name]["weight"]  # [out_ch, in_ch, kH, kW]
        conv_b = self.weights[conv_name].get("bias", np.zeros(conv_w.shape[0]))

        bn_gamma = self.weights[bn_name]["gamma"]           # [out_ch]
        bn_beta = self.weights[bn_name]["beta"]             # [out_ch]
        bn_mean = self.weights[bn_name]["running_mean"]     # [out_ch]
        bn_var = self.weights[bn_name]["running_var"]       # [out_ch]
        bn_eps = self.weights[bn_name].get("eps", 1e-5)

        # W' = W * (γ / √(σ² + ε))
        scale = bn_gamma / np.sqrt(bn_var + bn_eps)
        new_weight = conv_w * scale[:, None, None, None]

        # b' = γ * (b - μ) / √(σ² + ε) + β
        new_bias = scale * (conv_b - bn_mean) + bn_beta

        return {
            "weight": new_weight,
            "bias": new_bias
        }

    def execute(self) -> tuple[list, dict]:
        new_structure = []
        new_weights = dict(self.weights)
        skip_next = False

        for i, layer in enumerate(self.structure):
            if skip_next:
                skip_next = False
                continue

            layer_type = layer.get("type", "")
            next_layer = self.structure[i + 1] if i + 1 < len(self.structure) else None
            next_type = next_layer.get("type", "") if next_layer else ""

            if layer_type == LayerType.Conv2d.value and next_type == LayerType.BatchNorm.value:
                conv_name = layer["name"]
                bn_name = next_layer["name"]

                # Пересчитываем веса
                new_weights[conv_name] = self._fold(conv_name, bn_name)

                # Удаляем веса BN — они больше не нужны
                del new_weights[bn_name]

                # Обновляем тип слоя, BN исчезает
                new_layer = dict(layer)
                new_layer["type"] = LayerType.Conv2d.value
                new_structure.append(new_layer)
                skip_next = True

            else:
                new_structure.append(layer)

        return new_structure, new_weights