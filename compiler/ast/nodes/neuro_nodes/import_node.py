from compiler.ast.nodes.node import Node
from compiler.common.token import Token
from compiler.common.token_type import TokenType


class ImportNode(Node):
    # Что это вообще???
    def __init__(self, token: Token):
        if token.token_type != TokenType.WORD:
            raise Exception("ImportNode: token is not Word")

        self.token = token

    def execute(self):
        # Достать из файла данные
        return None
