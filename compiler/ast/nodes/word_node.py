from compiler.ast.nodes.node import Node
from compiler.lexer.token import Token
from compiler.lexer.token_type import TokenType


class WordNode(Node):
    def __init__(self, word: Token):
        if word.token_type != TokenType.WORD:
            raise Exception("WordNode: Token type is wrong")

        self.word = word

    def is_key_word(self):
        return self.word not in []
