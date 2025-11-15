from enum import Enum
from compiler.common.token_type import TokenType


STRING_OPERATOR = "\""
NEW_LINE_OPERATOR = "\n"


class Operator(Enum):
    PLUS = ("+", TokenType.PLUS)
    MINUS = ("-", TokenType.MINUS)
    ASSIGN = ("=", TokenType.ASSIGN)
    LEFT_PARENTHESES = ("(", TokenType.LEFT_PARENTHESES)
    RIGHT_PARENTHESES = (")", TokenType.RIGHT_PARENTHESES)
    COMMA = (",", TokenType.COMMA)
    # LEFT_BRACKET = ("[", TokenType.LEFT_BRACKET)
    # RIGHT_BRACKET = ("]", TokenType.RIGHT_BRACKET)
    LEFT_BRACE = ("{", TokenType.LEFT_BRACE)
    RIGHT_BRACE = ("}", TokenType.RIGHT_BRACE)
    MULTIPLICATION = ("*", TokenType.MULTIPLICATION)
    DIVISION = ("/", TokenType.DIVISION)
    LINK = ("->", TokenType.LINK)
    REVERSE_LINK = ("<-", TokenType.REVERSE_LINK)
    LAYER_START = ("[", TokenType.LAYER_START)
    LAYER_END = ("]", TokenType.LAYER_END)
    STRING = (STRING_OPERATOR, TokenType.STRING)
    NEW_LINE_SEPARATOR = (NEW_LINE_OPERATOR, TokenType.NEW_LINE_SEPARATOR)


def get_token_type_by_text(text: str):
    return next((operator.value[1] for operator in Operator if operator.value[0] == text), None)


OPERATORS_VALUE = [operator.value[0] for operator in Operator]
OPERATORS_NAME = [operator.name for operator in Operator]
OPERATORS_DICT = [{operator.name: operator.value} for operator in Operator]
OPERATORS = [operator.value[0] for operator in Operator] + ["<"]
