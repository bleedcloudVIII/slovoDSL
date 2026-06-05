from compiler.ast.nodes.common_nodes.word_node import WordNode
from compiler.ast.nodes.node import Node
from compiler.ast.nodes.common_nodes.number_node import NumberNode
from typing import Optional

from netopt.enums import LayerType


class BatchNormNode(Node):
    def __init__(
        self,
        eps: Optional[NumberNode] = None,
        momentum: Optional[NumberNode] = None,
        dependency: Optional[WordNode] = None
    ):
        self.eps = eps
        self.momentum = momentum
        self.dependency = dependency

    def execute(self):
        return None

    def __str__(self):
        return f"BatchNormNode<{self.eps}, {self.momentum}>"

    def __repr__(self):
        return f"BatchNormNode<{self.eps}, {self.momentum}>"

    def to_dict(self) -> dict:
        return {
            "type": LayerType.BatchNorm.value,
            "eps": self.eps.execute() if self.eps else 1e-5,
            "momentum": self.momentum.execute() if self.momentum else 0.1,
            "dependency": self.dependency.token.token_text if self.dependency else None
        }
