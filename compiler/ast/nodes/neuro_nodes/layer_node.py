from compiler.ast.nodes.node import Node
from compiler.ast.nodes.common_nodes.number_node import NumberNode
from compiler.ast.nodes.common_nodes.word_node import WordNode
from typing import Optional


class LayerNode(Node):
    # TODO Свободные члены или типа того
    def __init__(self, neurons_count: Optional[NumberNode], function: Optional[WordNode]):
        if neurons_count and not isinstance(neurons_count, NumberNode):
            raise Exception("LayerNode: neurons_count is not a NumberNode")

        if function and not isinstance(function, WordNode):
            raise Exception("LayerNode: functino is not a WordNode")

        self.neurons_count = neurons_count
        self.function = function

    def execute(self):
        # TODO Что-то делать
        return None

    def __str__(self):
        return f"LayerNode<{self.neurons_count.token.token_text if self.neurons_count else None}, {self.function.word.token_text if self.function else None }>"

    def __repr__(self):
        return f"ReverseLinkNode<{self.left}, {self.right}>"
