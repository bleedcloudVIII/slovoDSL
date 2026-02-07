from enum import Enum
# from compiler.ast.nodes.neuro_nodes.layer_node import LayerNode
from compiler.ast.nodes.node import Node


class KeyWord(Enum):
    # LAYER = ("layer", LayerNode)
    # Пока такого нет
    pass


def get_node_by_word(text: str) -> Node:
    return next((key_word.value[1] for key_word in KeyWord if key_word.value[0] == text), None)


KEY_WORDS_VALUE_NAME = [key_word.value[0] for key_word in KeyWord]
print(KEY_WORDS_VALUE_NAME)
