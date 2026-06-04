from compiler.ast.nodes.node import Node
from compiler.ast.nodes.common_nodes.number_node import NumberNode
from compiler.ast.nodes.common_nodes.list_node import ListNode
from typing import Optional

from netopt.enums import LayerType


class DropoutNode(Node):
    def __init__(
        self,
        p: Optional[NumberNode] = None,
        dependencies: Optional[ListNode] = []
    ):
        self.p = p
        self.dependencies = dependencies

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
                "p": self.p.value if self.p else 0.5,
            },
            "dependencies": [d.execute() for d in self.dependencies.expressions]
        }
