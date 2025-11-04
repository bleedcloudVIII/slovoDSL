from compiler.ast.nodes.node import Node
from compiler.common.token import Token
from compiler.common.token_type import TokenType
from compiler.common.key_words import KEY_WORDS_VALUE_NAME


class WordNode(Node):
    def __init__(self, word: Token):
        if word.token_type != TokenType.WORD:
            raise Exception("WordNode: Token type is wrong")

        self.word = word

    def is_key_word(self):
        return self.word.token_text not in KEY_WORDS_VALUE_NAME

    def execute(self):
        if not self.is_key_word:
            raise Exception("WordNode: cannot execute unrecognized key word")

        return None
