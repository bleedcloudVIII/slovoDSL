from compiler.ast.nodes.node import Node
from compiler.ast.nodes.common_nodes.number_node import NumberNode
from compiler.ast.nodes.common_nodes.list_node import ListNode
from typing import Optional

from netopt.enums import LayerType


class BatchNormNode(Node):
    def __init__(
        self,
        eps: Optional[NumberNode] = None,
        momentum: Optional[NumberNode] = None,
        dependencies: Optional[ListNode] = None
    ):
        self.eps = eps
        self.momentum = momentum
        self.dependencies = dependencies

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
            "dependencies": [d.token.token_text for d in self.dependencies.expressions] if self.dependencies else []
        }
