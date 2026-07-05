import numpy as np

from netopt.enums import LayerType


class WeightPruning:
    def __init__(self, structure: list, weights: dict, threshold: float = 0.01):
        self.structure = structure
        self.weights = weights
        self.threshold = threshold

    def _prune_conv(self, name: str) -> dict:
        weight = self.weights[name]["weight"]  # [out_ch, in_ch, kH, kW]
        bias = self.weights[name].get("bias", None)

        # Считаем L2 норму каждого выходного канала
        channel_norms = np.sqrt((weight ** 2).sum(axis=(1, 2, 3)))

        # Маска каналов которые оставляем
        keep_mask = channel_norms > self.threshold

        new_weight = weight[keep_mask]
        new_bias = bias[keep_mask] if bias is not None else None

        pruned = int((~keep_mask).sum())

        return {
            "weight": new_weight,
            "bias": new_bias,
            "keep_mask": keep_mask,
            "pruned_channels": pruned
        }

    def _prune_linear(self, name: str) -> dict:
        weight = self.weights[name]["weight"]  # [out, in]
        bias = self.weights[name].get("bias", None)

        # Считаем L2 норму каждого выходного нейрона
        neuron_norms = np.sqrt((weight ** 2).sum(axis=1))

        # Маска нейронов которые оставляем
        keep_mask = neuron_norms > self.threshold

        new_weight = weight[keep_mask]
        new_bias = bias[keep_mask] if bias is not None else None

        pruned = int((~keep_mask).sum())

        return {
            "weight": new_weight,
            "bias": new_bias,
            "keep_mask": keep_mask,
            "pruned_neurons": pruned
        }

    def _prune_next_layer_inputs(self, name: str, keep_mask: np.ndarray):
        """Обновляем входные веса следующего слоя — его входы уменьшились"""
        if name not in self.weights:
            return

        weight = self.weights[name]["weight"]

        if weight.ndim == 4:
            # Conv2d: [out_ch, in_ch, kH, kW]
            self.weights[name]["weight"] = weight[:, keep_mask, :, :]
        elif weight.ndim == 2:
            # Linear: [out, in]
            self.weights[name]["weight"] = weight[:, keep_mask]

    def execute(self) -> tuple[list, dict, dict]:
        new_weights = {k: dict(v) for k, v in self.weights.items()}
        pruning_report = {}

        for i, layer in enumerate(self.structure):
            layer_type = layer.get("type", "")
            name = layer.get("name", "")

            if name not in new_weights:
                continue

            next_layer = self.structure[i + 1] if i + 1 < len(self.structure) else None
            next_name = next_layer.get("name", "") if next_layer else ""

            if layer_type == LayerType.Conv2d.value:
                result = self._prune_conv(name)
                keep_mask = result.pop("keep_mask")
                pruning_report[name] = result["pruned_channels"]

                new_weights[name]["weight"] = result["weight"]
                if result["bias"] is not None:
                    new_weights[name]["bias"] = result["bias"]

                # Обновляем входы следующего слоя
                if next_name:
                    self._prune_next_layer_inputs(next_name, keep_mask)

            elif layer_type == LayerType.Linear.value:
                result = self._prune_linear(name)
                keep_mask = result.pop("keep_mask")
                pruning_report[name] = result["pruned_neurons"]

                new_weights[name]["weight"] = result["weight"]
                if result["bias"] is not None:
                    new_weights[name]["bias"] = result["bias"]

                # Обновляем входы следующего слоя
                if next_name:
                    self._prune_next_layer_inputs(next_name, keep_mask)

        return self.structure, new_weights, pruning_report
