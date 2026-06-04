from enum import Enum
# from compiler.ast.nodes.neuro_nodes.layer_node import LayerNode
from compiler.ast.nodes.neuro_nodes.add_node import AddNode
from compiler.ast.nodes.neuro_nodes.batch_norm import BatchNormNode
from compiler.ast.nodes.neuro_nodes.concat_node import ConcatNode
from compiler.ast.nodes.neuro_nodes.dropout_node import DropoutNode
from compiler.ast.nodes.neuro_nodes.relu_node import ReLUNode
from compiler.ast.nodes.node import Node
from compiler.ast.nodes.neuro_nodes.dense_node import DenseNode
from compiler.ast.nodes.neuro_nodes.conv2d_node import Conv2dNode
from compiler.ast.nodes.neuro_nodes.max_pooling_node import MaxPoolingNode
from compiler.ast.nodes.neuro_nodes.avg_pooling_node import AvgPoolingNode


class KeyWord(Enum):
    DENSE = ("Dense", DenseNode)
    CONV2D = ("Conv2d", Conv2dNode)
    MAX_POOLING = ("MaxPooling", MaxPoolingNode)
    AVG_POOLING = ("AvgPooling", AvgPoolingNode)
    BATCH_NORM = ("BatchNorm", BatchNormNode)
    DROPOUT = ("Dropout", DropoutNode)
    RELU = ("ReLU", ReLUNode)
    ADD = ("Add", AddNode)
    CONCAT = ("Concat", ConcatNode)


def get_node_by_word(text: str) -> Node:
    return next((key_word.value[1] for key_word in KeyWord if key_word.value[0] == text), None)


KEY_WORDS_VALUE_NAME = [key_word.value[0] for key_word in KeyWord]
