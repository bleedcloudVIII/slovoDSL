from enum import Enum
from compiler.common.token_type import TokenType


class Operator(Enum):
    PLUS = ("+", TokenType.PLUS)
    MINUS = ("-", TokenType.MINUS)
    ASSIGN = ("=", TokenType.ASSIGN)
    LEFT_PARENTHESES = ("(", TokenType.LEFT_PARENTHESES)
    RIGHT_PARENTHESES = (")", TokenType.RIGHT_PARENTHESES)
    COMMA = (",", TokenType.COMMA)
    LEFT_BRACKET = ("[", TokenType.LEFT_BRACKET)
    RIGHT_BRACKET = ("]", TokenType.RIGHT_BRACKET)
    LEFT_BRACE = ("{", TokenType.LEFT_BRACE)
    RIGHT_BRACE = ("}", TokenType.RIGHT_BRACE)
    MULTIPLICATION = ("*", TokenType.MULTIPLICATION)
    DIVISION = ("/", TokenType.DIVISION)
    LINK = ("->", TokenType.LINK)
    LINK = ("<-", TokenType.REVERSE_LINK)
    LAYER_START = ("[", TokenType.LAYER_START)
    LAYER_END = ("]", TokenType.LAYER_END)


def get_token_type_by_text(text: str):
    return next((operator.value[1] for operator in Operator if operator.value[0] == text), None)


OPERATORS_VALUE = [operator.value[0] for operator in Operator]
OPERATORS_NAME = [operator.name for operator in Operator]
OPERATORS_DICT = [{operator.name: operator.value} for operator in Operator]
