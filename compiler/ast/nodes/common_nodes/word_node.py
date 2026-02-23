from compiler.ast.nodes.node import Node
from compiler.common.token import Token
from compiler.common.token_type import TokenType


class WordNode(Node):
    def __init__(self, word: Token):
        if word.token_type != TokenType.WORD:
            raise Exception("WordNode: Token type is wrong")

        word.token_text.strip()
        self.token = word

    def execute(self):
        pass

    def __str__(self):
        return f"WordNode<{self.token.token_text}>"

    def __repr__(self):
        return f"WordNode<{self.token.token_text}>"
