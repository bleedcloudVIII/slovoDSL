from compiler.ast.nodes.node import Node
from compiler.lexer.token import Token
from compiler.lexer.token_type import TokenType


class NumberNode(Node):
    def __init__(self, value: Token):
        if value.token_type != TokenType.NUMBER:
            raise Exception("NumberNode: Token not a number")
        self.value = value

    def execute(self):
        return int(self.value.token_text)
