from netopt.enums import LayerType


class IdentityOpt:
    def __init__(self, structure: list):
        self.structure = structure

    def _is_identity(self, layer: dict) -> bool:
        layer_type = layer.get("type", "")

        if layer_type == LayerType.Dropout.value:
            return layer.get("params", {}).get("p", 1.0) == 0.0

        return False

    def execute(self) -> list:
        return [layer for layer in self.structure if not self._is_identity(layer)]
