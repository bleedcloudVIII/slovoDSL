from enum import Enum

from compiler.ast.nodes.node import Node
from compiler.ast.nodes.common_nodes.number_node import NumberNode
from compiler.ast.nodes.common_nodes.list_node import ListNode
from typing import Optional

from compiler.common.token import Token
from compiler.common.token_type import TokenType
from netopt.enums import LayerType


class ConcatAxisType(Enum):
    BATCH = 0
    FEATURES_CHANNELS = 1
    HEIGHT = 2
    WIDTH = 3


DEFAULT_AXIS = NumberNode(Token(token_text=str(ConcatAxisType.FEATURES_CHANNELS.value), token_type=TokenType.NUMBER))


class ConcatNode(Node):
    def __init__(
        self,
        dependencies: Optional[ListNode] = None,
        axis: Optional[NumberNode] = None
    ):
        self.dependencies = dependencies

        if axis is None:
            axis = DEFAULT_AXIS

        self.axis = axis

    def execute(self):
        return None

    def __str__(self):
        return f"ConcatNode<axis={self.axis}>"

    def __repr__(self):
        return f"ConcatNode<axis={self.axis}>"

    def to_dict(self) -> dict:
        return {
            "type": LayerType.Concat.value,
            "axis": self.axis.execute() if self.axis else 1,
            "dependencies": [d.token.token_text for d in self.dependencies.expressions] if self.dependencies else []
        }
