from compiler.ast.nodes.node import Node
from compiler.ast.nodes.common_nodes.list_node import ListNode
from typing import Optional

from netopt.enums import LayerType


class ReLUNode(Node):
    def __init__(
        self,
        dependencies: Optional[ListNode] = None
    ):
        self.dependencies = dependencies

    def execute(self):
        return None

    def __str__(self):
        return "ReLUNode<>"

    def __repr__(self):
        return "ReLUNode<>"

    def to_dict(self) -> dict:
        return {
            "type": LayerType.ReLU.value,
            "dependencies": [d.execute() for d in self.dependencies.expressions] if self.dependencies else []
        }