from enum import Enum, auto


class TokenType(Enum):
    NUMBER = auto()
    WORD = auto()
    STRING = auto()

    PLUS = auto()
    MINUS = auto()
    ASSIGN = auto()
    LEFT_PARENTHESES = auto()
    RIGHT_PARENTHESES = auto()
    COMMA = auto()
    LEFT_BRACKET = auto()
    RIGHT_BRACKET = auto()
    LEFT_BRACE = auto()
    RIGHT_BRACE = auto()
    MULTIPLICATION = auto()
    DIVISION = auto()
