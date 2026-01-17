from compiler.ast.nodes.node import Node
from compiler.ast.nodes.common_nodes.word_node import WordNode
from compiler.common.token_type import TokenType


LINKS_OPERATORS_TOKEN_TYPE = [
    TokenType.LINK,
    TokenType.REVERSE_LINK
]


class LinkNode(Node):
    def __init__(self, left: Node, right: Node):
        self.left = left
        self.right = right

    def execute(self):
        left_value = self.left.execute()

        if isinstance(self.right, WordNode):
            self.right.set(left_value)

    def __str__(self):
        return f"LinkNode<{self.left}, {self.right}>"

    def __repr__(self):
        return f"LinkNode<{self.left}, {self.right}>"
