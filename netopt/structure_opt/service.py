from netopt.structure_opt.enums import LayerType


class StructureOpt:
    def __init__(self, structure: dict):
        self.structure = structure

    def _layer_type(self, layer: dict | None) -> str:
        if layer is not None:
            return layer.get("type", "")
        return ""

    def execute(self):
        index = 0
        new_structure = []

        skip_next_layer = False
        for item in self.structure:
            if skip_next_layer:
                continue

            current_type = self._layer_type(item)

            next_item = self.structure[index + 1] if len(self.structure) > index + 1 else None
            next_type = self._layer_type(next_item)

            new_type = None
            if current_type == LayerType.Conv2d.value and next_type == LayerType.BatchNorm.value:
                new_type = LayerType.Conv2d_BatchNorm.value
                new_value = {
                    "type": new_type
                }

                new_structure.append(new_value)
                index += 1
                skip_next_layer = True
            elif current_type == LayerType.Conv2d_BatchNorm.value and next_type == LayerType.ReLU.value:
                new_type = LayerType.C2B_ReLU.value
                new_value = {
                    "type": new_type
                }

                new_structure.append(new_value)
                index += 1
                skip_next_layer = True
            elif current_type == LayerType.Linear.value and next_type == LayerType.BatchNorm.value:
                new_type = LayerType.Linear_BarchNorm.value
                new_value = {
                    "type": new_type
                }

                new_structure.append(new_value)
                index += 1
                skip_next_layer = True
            elif current_type == LayerType.Linear.value and next_type == LayerType.ReLU.value:
                new_type = LayerType.Linear_ReLU.value
                new_value = {
                    "type": new_type
                }

                new_structure.append(new_value)
                index += 1
                skip_next_layer = True
            else:
                new_structure.append(item)
                skip_next_layer = False

            index += 1

        return new_structure
