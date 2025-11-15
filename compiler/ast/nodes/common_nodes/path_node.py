from compiler.ast.nodes.node import Node
from compiler.common.token import Token
from compiler.common.token_type import TokenType


class PathNode(Node):
    def __init__(self, path: Token):
        if path.token_type != TokenType.STRING:
            raise Exception("PathNode: Token not a string")
        self.path = path

    def execute(self):
        return None

    def __str__(self):
        return f"PathNode<{self.path.token_text}>"

    def __repr__(self):
        return f"PathNode<{self.path.token_text}>"
