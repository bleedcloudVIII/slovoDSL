from compiler.ast.nodes.node import Node
from compiler.ast.nodes.common_nodes.number_node import NumberNode
from compiler.ast.nodes.common_nodes.list_node import ListNode
from typing import Optional

from netopt.enums import LayerType


class ConcatNode(Node):
    def __init__(
        self,
        dependencies: Optional[ListNode] = None,
        axis: Optional[NumberNode] = None
    ):
        self.dependencies = dependencies
        self.axis = axis

# axis=0 — по batch
# axis=1 — по features/channels  ← чаще всего
# axis=2 — по высоте (для 2D)
# axis=3 — по ширине (для 2D)

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
            "dependencies": [d.execute() for d in self.dependencies.expressions] if self.dependencies else []
        }