from compiler.lexer.lexer import Lexer

code = "a = layer[50, 60, func]"
lexer = Lexer(code)

print(lexer.lexer_analysis())
