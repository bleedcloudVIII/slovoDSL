from compiler.token_type import TokenType


class Token:
    def __init__(self, token_type: TokenType, token_text: str):
        self.token_type = token_type
        self.token_text = token_text

    def __str__(self):
        return f"TokenType<{self.token_type}, {self.token_text}>"

    def __repr__(self):
        return f"TokenType<{self.token_type}, {self.token_text}>"
