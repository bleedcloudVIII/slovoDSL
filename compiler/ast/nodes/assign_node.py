from compiler.ast.nodes.node import Node
from compiler.lexer.token import Token
from compiler.lexer.token_type import TokenType

# TODO Сделать хранение переменных нормальным
VARIABLES = {}


class AssignNode(Node):
    def __init__(self, variable: Token, expression: Node):
        if variable.token_type != TokenType.STRING:
            raise Exception("AssignNode: variable is not string")

        if not isinstance(expression, Node):
            raise Exception("AssignNode: expression is not Node")

        self.variable = variable
        self.expression = expression

    def execute(self):
        expression_value = self.expression.execute()

        VARIABLES[self.variable] = expression_value

        return expression_value
