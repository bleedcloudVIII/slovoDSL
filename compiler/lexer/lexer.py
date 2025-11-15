from compiler.common.token_type import TokenType
from compiler.common.token import Token
from compiler.common.operators import OPERATORS_VALUE, get_token_type_by_text, STRING_OPERATOR, NEW_LINE_OPERATOR


class Lexer:
    def __init__(self, code: str):
        self.code = code
        self.position = 0
        self.tokens = []
        self.length = len(self.code)

    @property
    def current_symbol(self):
        return self.code[self.position]

    def tokenize_number(self):
        string = ""
        while self.current_symbol.isdigit():
            string += self.current_symbol
            self.position += 1

            if self.position >= self.length:
                break

        self.tokens.append(Token(TokenType.NUMBER, string))

    def tokenize_word(self):
        string = ""
        while self.current_symbol.isalpha():
            string += self.current_symbol
            self.position += 1

            if self.position >= self.length:
                break

        self.tokens.append(Token(TokenType.WORD, string))

    def _get_operator_token(self, text: str):
        token_type = get_token_type_by_text(text)

        if not token_type:
            raise Exception

        return Token(token_type, text)

    def tokenize_operator(self):
        string = ""
        while (string + self.current_symbol) in OPERATORS_VALUE:
            string += self.current_symbol
            self.position += 1

            if self.position >= self.length:
                break

        self.tokens.append(self._get_operator_token(string))

    def tokenize_string(self):
        string = ""
        self.position += 1
        while self.current_symbol != STRING_OPERATOR:
            string += self.current_symbol
            self.position += 1

            if self.position >= self.length:
                break

        if self.position < self.length:
            self.position += 1

        self.tokens.append(Token(TokenType.STRING, string))

    def tokenize_new_line(self):
        self.tokens.append(Token(TokenType.NEW_LINE_SEPARATOR, NEW_LINE_OPERATOR))
        self.position += 1

    def lexer_analysis(self):
        while self.position < self.length:
            if self.current_symbol in OPERATORS_VALUE and self.current_symbol == NEW_LINE_OPERATOR:
                self.tokenize_new_line()
            if self.current_symbol in OPERATORS_VALUE and self.current_symbol == STRING_OPERATOR:
                self.tokenize_string()
            elif self.current_symbol in OPERATORS_VALUE:
                self.tokenize_operator()
            elif self.current_symbol.isdigit():
                self.tokenize_number()
            elif self.current_symbol.isalpha():
                self.tokenize_word()
            else:
                # spaces
                self.position += 1

        return self.tokens
