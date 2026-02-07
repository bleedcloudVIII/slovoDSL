from compiler.ast.nodes.node import Node
from compiler.common.token import Token
from compiler.common.token_type import TokenType


class WordNode(Node):
    def __init__(self, word: Token):
        if word.token_type != TokenType.WORD:
            raise Exception("WordNode: Token type is wrong")

        self.token = word

    @property
    def is_key_word(self):
        pass
        # from compiler.common.key_words import KEY_WORDS_VALUE_NAME
        # return self.token.token_text in KEY_WORDS_VALUE_NAME

    def is_function(self):
        return False

    def execute(self):
        pass
        # if not self.is_key_word:
        #     return VARIABLES[self.token.token_text]

        # if not self.is_function():
        #     pass

        # По идеи сюда никак не попадёт
        # raise Exception("WordNode: unrecognized word")

    def set(self, new_value):
        pass
        # VARIABLES[self.token.token_text] = new_value
        # return None

    def get(self):
        pass
        # return self.execute()

    def __str__(self):
        return f"WordNode<{self.token.token_text}>"

    def __repr__(self):
        return f"WordNode<{self.token.token_text}>"
