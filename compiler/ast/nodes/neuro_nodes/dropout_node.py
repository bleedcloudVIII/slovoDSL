from compiler.ast.nodes.common_nodes.word_node import WordNode
from compiler.ast.nodes.node import Node
from compiler.ast.nodes.common_nodes.number_node import NumberNode
from typing import Optional

from netopt.enums import LayerType


class DropoutNode(Node):
    def __init__(
        self,
        p: Optional[NumberNode] = None,
        dependency: Optional[WordNode] = None
    ):
        self.p = p
        self.dependency = dependency

    def execute(self):
        return None

    def __str__(self):
        return f"DropoutNode<{self.p}>"

    def __repr__(self):
        return f"DropoutNode<{self.p}>"

    def to_dict(self) -> dict:
        return {
            "type": LayerType.Dropout.value,
            "params": {
                "p": self.p.execute() if self.p else 0.5,
            },
            "dependency": self.dependency.token.token_text if self.dependency else None
        }
