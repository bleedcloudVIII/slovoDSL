from compiler.ast.nodes.node import Node
from compiler.ast.nodes.common_nodes.number_node import NumberNode
from compiler.ast.nodes.common_nodes.word_node import WordNode
from compiler.ast.nodes.common_nodes.list_node import ListNode
from typing import Optional


class DenseNode(Node):
    def __init__(
        self,
        input_size: Optional[NumberNode] = None,
        function: Optional[WordNode] = None,
        bias: Optional[ListNode | WordNode] = None
    ):
        self.input_size = input_size
        self.function = function
        self.bias = bias

    def execute(self):
        return None

    def __str__(self):
        input_size = self.input_size or None
        function = self.function.token.token_text if self.function else None
        bias = self.bias

        if isinstance(self.bias, WordNode):
            bias = self.bias.token.token_text

        if isinstance(self.bias, ListNode):
            bias = str(self.bias)

        return f"DenseNode<{input_size}, {function}, {bias}>"

    def __repr__(self):
        input_size = self.input_size or None
        function = self.function.token.token_text if self.function else None
        bias = self.bias

        if isinstance(self.bias, WordNode):
            bias = self.bias.token.token_text

        if isinstance(self.bias, ListNode):
            bias = str(self.bias)

        return f"DenseNode<{input_size}, {function}, {bias}>"
