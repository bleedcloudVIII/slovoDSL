from compiler.ast.nodes.node import Node
from compiler.ast.nodes.common_nodes.word_node import WordNode
from compiler.ast.nodes.common_nodes.list_node import ListNode
from typing import Optional

from netopt.enums import LayerType


class Conv2dNode(Node):
    def __init__(
        self,
        kernel_size: Optional[ListNode | WordNode] = None,
        offset: Optional[ListNode | WordNode] = None,
        padding: Optional[ListNode | WordNode] = None,
        stride: Optional[ListNode | WordNode] = None,
        dependency: Optional[WordNode] = None
    ):
        self.kernel_size = kernel_size
        self.offset = offset
        self.padding = padding
        self.stride = stride
        self.dependency = dependency

    def execute(self):
        return None

    def __str__(self):
        return f"Conv2DNode<{self.kernel_size}, {self.offset}, {self.padding}, {self.stride}>"

    def __repr__(self):
        return f"Conv2DNode<{self.kernel_size}, {self.offset}, {self.padding}, {self.stride}>"

    def to_dict(self) -> dict:
        return {
            "type": LayerType.Conv2d.value,
            "kernel_size": self.kernel_size.execute() if self.kernel_size else [1, 1],
            "offset": self.offset.execute() if self.offset else [0, 0],
            "padding": self.padding.execute() if self.padding else [0, 0],
            "stride": self.stride.execute() if self.stride else [1, 1],
            "dependency": self.dependency.token.token_text if self.dependency else None
        }
