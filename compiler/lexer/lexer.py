from compiler.lexer.token_type import TokenType
from compiler.lexer.token import Token
from compiler.lexer.operators import OPERATORS_VALUE, get_token_type_by_text


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
        str = ""
        while self.current_symbol.isdigit():
            str += self.current_symbol
            self.position += 1

            if self.position >= self.length:
                break

        self.tokens.append(Token(TokenType.NUMBER, str))

    def tokenize_word(self):
        str = ""
        while self.current_symbol.isalpha():
            str += self.current_symbol
            self.position += 1

            if self.position >= self.length:
                break

        self.tokens.append(Token(TokenType.STRING, str))

    def _get_operator_token(self, text: str):
        token_type = get_token_type_by_text(text)

        if not token_type:
            raise Exception

        return Token(token_type, text)

    def tokenize_operator(self):
        str = ""
        while (str + self.current_symbol) in OPERATORS_VALUE:
            str += self.current_symbol
            self.position += 1

            if self.position >= self.length:
                break

        self.tokens.append(self._get_operator_token(str))

    def lexer_analysis(self):
        while self.position < self.length:
            if (self.current_symbol.isdigit()):
                self.tokenize_number()
            elif (self.current_symbol.isalpha()):
                self.tokenize_word()
            elif (self.current_symbol in OPERATORS_VALUE):
                self.tokenize_operator()
            else:
                # spaces
                self.position += 1

        return self.tokens
