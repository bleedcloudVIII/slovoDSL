from compiler.lexer import Lexer

code = "2 + 5 = a + [v + {4 + 0 }]  - 2"
lexer = Lexer(code)

print(lexer.lexer_analysis())
