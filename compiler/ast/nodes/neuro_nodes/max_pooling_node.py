from compiler.ast.nodes.node import Node
from compiler.ast.nodes.common_nodes.number_node import NumberNode
from compiler.ast.nodes.common_nodes.list_node import ListNode
from typing import Optional

from netopt.enums import LayerType


class MaxPoolingNode(Node):
    def __init__(
        self,
        pool_size: Optional[NumberNode] = None,
        stride: Optional[NumberNode] = None,
        dependency: Optional[ListNode] = None
    ):
        self.pool_size = pool_size
        self.stride = stride or pool_size
        self.dependency = dependency

    def execute(self):
        return None

    def __str__(self):
        return f"MaxPoolingNode<{self.pool_size}, stride={self.stride}>"

    def __repr__(self):
        return f"MaxPoolingNode<{self.pool_size}, stride={self.stride}>"

    def to_dict(self) -> dict:
        return {
            "type": LayerType.MaxPooling.value,
            "pool_size": self.pool_size.execute() if self.pool_size else 2,
            "stride": self.stride.execute() if self.stride else 2,
            "dependency": self.dependency.token.token_text if self.dependency else None
        }
