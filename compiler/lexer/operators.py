from enum import Enum
from compiler.lexer.token_type import TokenType


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


def get_token_type_by_text(text: str):
    return next((operator.value[1] for operator in Operator if operator.value[0] == text), None)


OPERATORS_VALUE = [operator.value[0] for operator in Operator]
OPERATORS_NAME = [operator.name for operator in Operator]
OPERAATORS_DICT = [{operator.name: operator.value} for operator in Operator]
