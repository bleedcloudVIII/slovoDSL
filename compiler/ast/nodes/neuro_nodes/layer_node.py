from compiler.ast.nodes.node import Node
from compiler.ast.nodes.common_nodes.number_node import NumberNode
from compiler.ast.nodes.common_nodes.word_node import WordNode
from typing import Optional


class LayerNode(Node):
    def __init__(self, neurons_count: Optional[NumberNode], function: Optional[WordNode], bias: Optional[WordNode]):
        if function and not isinstance(function, WordNode):
            raise Exception("LayerNode: function is not a WordNode")

        if bias and not isinstance(bias, WordNode):
            raise Exception("LayerNode: bias is not a WordNode")

        self.neurons_count = neurons_count
        self.function = function
        self.bias = bias

    def execute(self):
        # TODO Что-то делать
        return None

    def __str__(self):
        neurons_count = self.neurons_count if self.neurons_count else None
        func = self.function.token.token_text if self.function else None
        bias = self.bias.token.token_text if self.bias else None
        return f"LayerNode<{neurons_count}, {func}, {bias}>"

    def __repr__(self):
        neurons_count = self.neurons_count if self.neurons_count else None
        func = self.function.token.token_text if self.function else None
        bias = self.bias.token.token_text if self.bias else None
        return f"LayerNode<{neurons_count}, {func}, {bias}>"
