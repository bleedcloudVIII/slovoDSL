import numpy as np

from netopt.enums import LayerType


class NormFolding:
    def __init__(self, structure: list, weights: dict):
        self.structure = structure
        self.weights = weights

    def _fold_conv(self, conv_name: str, bn_name: str) -> dict:
        conv_w = self.weights[conv_name]["weight"]  # [out_ch, in_ch, kH, kW]
        conv_b = self.weights[conv_name].get("bias", np.zeros(conv_w.shape[0]))

        bn_gamma = self.weights[bn_name]["gamma"]
        bn_beta = self.weights[bn_name]["beta"]
        bn_mean = self.weights[bn_name]["running_mean"]
        bn_var = self.weights[bn_name]["running_var"]
        bn_eps = self.weights[bn_name].get("eps", 1e-5)

        scale = bn_gamma / np.sqrt(bn_var + bn_eps)
        new_weight = conv_w * scale[:, None, None, None]
        new_bias = scale * (conv_b - bn_mean) + bn_beta

        return {
            "weight": new_weight,
            "bias": new_bias
        }

    def _fold_linear(self, linear_name: str, bn_name: str) -> dict:
        linear_w = self.weights[linear_name]["weight"]  # [out, in]
        linear_b = self.weights[linear_name].get("bias", np.zeros(linear_w.shape[0]))

        bn_gamma = self.weights[bn_name]["gamma"]
        bn_beta = self.weights[bn_name]["beta"]
        bn_mean = self.weights[bn_name]["running_mean"]
        bn_var = self.weights[bn_name]["running_var"]
        bn_eps = self.weights[bn_name].get("eps", 1e-5)

        # Формула та же что для Conv2d
        scale = bn_gamma / np.sqrt(bn_var + bn_eps)
        new_weight = linear_w * scale[:, None]
        new_bias = scale * (linear_b - bn_mean) + bn_beta

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

                new_weights[conv_name] = self._fold_conv(conv_name, bn_name)
                del new_weights[bn_name]

                new_layer = dict(layer)
                new_structure.append(new_layer)
                skip_next = True

            elif layer_type == LayerType.Linear.value and next_type == LayerType.BatchNorm.value:
                linear_name = layer["name"]
                bn_name = next_layer["name"]

                new_weights[linear_name] = self._fold_linear(linear_name, bn_name)
                del new_weights[bn_name]

                new_layer = dict(layer)
                new_structure.append(new_layer)
                skip_next = True

            else:
                new_structure.append(layer)

        return new_structure, new_weights
