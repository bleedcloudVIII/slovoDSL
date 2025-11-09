from compiler.ast.nodes.node import Node
from compiler.common.token import Token
from compiler.common.token_type import TokenType
from compiler.common.key_words import KEY_WORDS_VALUE_NAME
from compiler.ast.nodes.common_nodes.assign_node import VARIABLES


class WordNode(Node):
    def __init__(self, word: Token):
        if word.token_type != TokenType.WORD:
            raise Exception("WordNode: Token type is wrong")

        self.token = word

    @property
    def is_key_word(self):
        return self.token.token_text in KEY_WORDS_VALUE_NAME

    def is_function(self):
        return False

    def execute(self):
        if not self.is_key_word:
            return VARIABLES[self.token.token_text]

        if not self.is_funciton():
            pass

        # По идеи сюда никак не попадёт
        raise Exception("WordNode: unrecognized word")

    def set(self, new_value):
        VARIABLES[self.token.token_text] = new_value
        return None

    def get(self):
        return self.execute()

    def __str__(self):
        return f"WordNode<{self.token.token_text}>"

    def __repr__(self):
        return f"WordNode<{self.token.token_text}>"
