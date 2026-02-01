from compiler.common.token_type import TokenType


class Token:
    def __init__(self, token_type: TokenType, token_text: str):
        self.token_type = token_type
        self.token_text = token_text

    def __str__(self):
        if self.token_type == TokenType.NEW_LINE_SEPARATOR:
            return f"Token<{self.token_type}>"
        return f"Token<{self.token_type}, {self.token_text}>"

    def __repr__(self):
        if self.token_type == TokenType.NEW_LINE_SEPARATOR:
            return f"Token<{self.token_type}>\n"
        return f"Token<{self.token_type.name}, {self.token_text}>"
