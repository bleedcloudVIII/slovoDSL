from compiler.lexer.lexer import Lexer
from compiler.ast.nodes.common_nodes.bin_operator_node import BinOperatorNode
from compiler.ast.nodes.common_nodes.number_node import NumberNode
from compiler.common.token import Token
from compiler.common.token_type import TokenType
from compiler.ast.parser import Parser

b = BinOperatorNode(
    operator=Token(TokenType.MINUS, "-"),
    left_value=NumberNode(Token(TokenType.NUMBER, "50")),
    right_value=NumberNode(Token(TokenType.NUMBER, "25"))
)   # 50 - 25 = 25

a = BinOperatorNode(
    operator=Token(TokenType.MULTIPLICATION, "+"),
    left_value=NumberNode(Token(TokenType.NUMBER, "50")),
    right_value=b
)   # 50 * 25 = 1250

c = BinOperatorNode(
    operator=Token(TokenType.MULTIPLICATION, "+"),
    left_value=a,
    right_value=b
)   # 25 * 1250 = 31250

print(a.execute())
print(b.execute())
print(c.execute())

# code = "a = layer[50, 60, func]"
# code = """a = 9 + 2
# b = 2 - 1
# "test.txt" -> c
# a <- c
# []
# [50]
# [60, sigmoid]"""
code = """
[]
[30]
[50, log]
[12+123, max]
a -> []
b -> [60 * 2]
c -> [60, sigmoid]
c -> a
"""
lexer = Lexer(code)

tokens = lexer.lexer_analysis()
print(tokens)

parser = Parser(tokens)
nodes = parser.parse()

for n in nodes:
    print(n)

# print(nodes)
# print(nodes[0].execute())
