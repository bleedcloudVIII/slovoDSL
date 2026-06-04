from netopt.enums import LayerType


class StructureOpt:
    def __init__(self, structure: dict):
        self.structure = structure

    def _layer_type(self, layer: dict | None) -> str:
        if layer is not None:
            return layer.get("type", "")
        return ""

    def _get(self, index: int) -> dict | None:
        if 0 <= index < len(self.structure):
            return self.structure[index]
        return None

    def execute(self):
        new_structure = []
        index = 0

        while index < len(self.structure):
            t0 = self._layer_type(self._get(index))
            t1 = self._layer_type(self._get(index + 1))
            t2 = self._layer_type(self._get(index + 2))

            C = LayerType.Conv2d.value
            L = LayerType.Linear.value
            BN = LayerType.BatchNorm.value
            RL = LayerType.ReLU.value

            if t0 == C and t1 == BN and t2 == RL:
                new_structure.append({"type": LayerType.Conv2d_BatchNorm_ReLU.value})
                index += 3

            elif t0 == L and t1 == BN and t2 == RL:
                new_structure.append({"type": LayerType.Linear_BatchNorm_ReLU.value})
                index += 3

            elif t0 == C and t1 == BN:
                new_structure.append({"type": LayerType.Conv2d_BatchNorm.value})
                index += 2

            elif t0 == C and t1 == RL:
                new_structure.append({"type": LayerType.Conv2d_ReLU.value})
                index += 2

            elif t0 == L and t1 == BN:
                new_structure.append({"type": LayerType.Linear_BatchNorm.value})
                index += 2

            elif t0 == L and t1 == RL:
                new_structure.append({"type": LayerType.Linear_ReLU.value})
                index += 2

            else:
                new_structure.append(self.structure[index])
                index += 1

        return new_structure
