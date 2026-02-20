from compiler.ast.nodes.node import Node
from compiler.ast.nodes.common_nodes.number_node import NumberNode
from compiler.ast.nodes.common_nodes.word_node import WordNode
from typing import Optional


class KernelNode(Node):
    def __init__(self, columns: Optional[NumberNode], rows: Optional[WordNode], function: Optional[WordNode]):
        if function and not isinstance(function, WordNode):
            raise Exception("KernelNode: function is not a WordNode")

        # if bias and not isinstance(bias, WordNode):
        #     raise Exception("LayerNode: bias is not a WordNode")

        self.rows = rows
        self.columns = columns
        self.function = function

    def execute(self):
        return None

    def __str__(self):
        rows = self.rows or None
        columns = self.columns or None
        func = self.function.token.token_text if self.function else None

        return f"KernelNode<{columns}, {rows}, {func}>"

    def __repr__(self):
        rows = self.rows or None
        columns = self.columns or None
        func = self.function.token.token_text if self.function else None

        return f"KernelNode<{columns}, {rows}, {func}>"
