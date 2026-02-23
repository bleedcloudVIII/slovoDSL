from compiler.ast.nodes.node import Node
from compiler.ast.nodes.common_nodes.word_node import WordNode
from compiler.ast.nodes.common_nodes.list_node import ListNode
from typing import Optional


class Conv2dNode(Node):
    def __init__(
        self,
        kernel_size: Optional[ListNode | WordNode] = None,
        offset: Optional[ListNode | WordNode] = None,
        padding: Optional[ListNode | WordNode] = None
    ):
        self.kernel_size = kernel_size
        self.offset = offset
        self.padding = padding

    def execute(self):
        return None

    def __str__(self):
        return f"Conv2DNode<{self.kernel_size}, {self.offset}, {self.padding}>"

    def __repr__(self):
        return f"Conv2DNode<{self.kernel_size}, {self.offset}, {self.padding}>"
