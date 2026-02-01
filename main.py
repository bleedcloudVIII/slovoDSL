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
    operator=Token(TokenType.MULTIPLICATION, "*"),
    left_value=NumberNode(Token(TokenType.NUMBER, "50")),
    right_value=b
)   # 50 * 25 = 1250

c = BinOperatorNode(
    operator=Token(TokenType.MULTIPLICATION, "*"),
    left_value=a,
    right_value=b
)   # 25 * 1250 = 31250


# print(a.execute())
# print(b.execute())
# print(c.execute())
# code = "[50, 60, func]"
# code = """a = 9 + 2
# b = 2 - 1

# a <- c

# code = """[60+ 10, ii]"""

# code = """
# []
# [50 / 2]
# [,func]
# [60 + 10 * 2, sigmoid]
# """

# code = """60 + 90 - 20 / 10 * 3"""
#  60 + 90 - 2 * 3
#  60 + 90 - 6
#  150 - 6
#  144
# 129


# code = """ a -> 70 + 20 """
# code = """ 30 + 10 -> t """

# code = """60 + 90 - 20"""

# code = """ "path/to/file.txt" """

code = """ 60 + 20 - 30 * 2 + 70 / 35 """
# 80 - 60 + 70 / 35
# 20 + 2
# 22

lexer = Lexer(code)

tokens = lexer.lexer_analysis()
print(tokens)

parser = Parser(tokens)
nodes = parser.parse()
print("-----")
for n in nodes:
    print(n)
# print(nodes[1].execute())

# print(nodes)
print(nodes[0].execute())
