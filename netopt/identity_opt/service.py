from netopt.enums import LayerType


class IdentityOpt:
    """ Оптимизацтор тождественных слоёв, то есть удаление слоёв, которые не оказывают влияния на результат работы модели. """
    def __init__(self, structure: list):
        self.structure = structure

    def _is_identity(self, layer: dict) -> bool:
        layer_type = layer.get("type", "")

        if layer_type == LayerType.Dropout.value:
            return True

        return False

    def execute(self) -> list:
        return [layer for layer in self.structure if not self._is_identity(layer)]
