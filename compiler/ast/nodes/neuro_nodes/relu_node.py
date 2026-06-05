from compiler.ast.nodes.common_nodes.word_node import WordNode
from compiler.ast.nodes.node import Node
from typing import Optional

from netopt.enums import LayerType


class ReLUNode(Node):
    def __init__(
        self,
        dependency: Optional[WordNode] = None
    ):
        self.dependency = dependency

    def execute(self):
        return None

    def __str__(self):
        return "ReLUNode<>"

    def __repr__(self):
        return "ReLUNode<>"

    def to_dict(self) -> dict:
        return {
            "type": LayerType.ReLU.value,
            "dependency": self.dependency.token.token_text if self.dependency else None
        }
