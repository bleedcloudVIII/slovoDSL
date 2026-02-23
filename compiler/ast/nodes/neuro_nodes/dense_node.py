from compiler.ast.nodes.node import Node
from compiler.ast.nodes.common_nodes.number_node import NumberNode
from compiler.ast.nodes.common_nodes.word_node import WordNode
from compiler.ast.nodes.common_nodes.list_node import ListNode
from typing import Optional


class DenseNode(Node):
    def __init__(
        self,
        input_size: Optional[NumberNode] = None,
        value: Optional[WordNode | ListNode] = None,
        dependencies: Optional[ListNode] = []
    ):
        self.input_size = input_size
        self.value = value
        self.dependencies = dependencies

    def execute(self):
        return None

    def __str__(self):
        return f"DenseNode<{self.input_size}, {self.value}>"

    def __repr__(self):
        return f"DenseNode<{self.input_size}, {self.value}>"
