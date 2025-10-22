from enum import Enum


class TokenType(Enum):
    NUMBER = 0
    STRING = 1

    PLUS = 2
    MINUS = 3
    ASSIGN = 4
    LEFT_PARENTHESES = 5
    RIGHT_PARENTHESES = 6
    COMMA = 7
    LEFT_BRACKET = 8
    RIGHT_BRACKET = 9
    LEFT_BRACE = 10
    RIGHT_BRACE = 11
    MULTIPLICATION = 12
    DIVISION = 13
