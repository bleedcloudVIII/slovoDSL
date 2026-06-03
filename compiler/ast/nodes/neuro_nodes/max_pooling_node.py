from compiler.ast.nodes.node import Node
from compiler.ast.nodes.common_nodes.number_node import NumberNode
from compiler.ast.nodes.common_nodes.list_node import ListNode
from typing import Optional


class MaxPoolingNode(Node):
    def __init__(
        self,
        pool_size: Optional[NumberNode] = None,
        stride: Optional[NumberNode] = None,
        dependencies: Optional[ListNode] = []
    ):
        self.pool_size = pool_size
        self.stride = stride or pool_size
        self.dependencies = dependencies

    def execute(self):
        return None

    def __str__(self):
        return f"MaxPoolingNode<{self.pool_size}, stride={self.stride}>"

    def __repr__(self):
        return f"MaxPoolingNode<{self.pool_size}, stride={self.stride}>"
