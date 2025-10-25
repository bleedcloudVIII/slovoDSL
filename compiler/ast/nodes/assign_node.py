from compiler.ast.nodes.node import Node
from compiler.lexer.token import Token
from compiler.lexer.token_type import TokenType


class AssignNode(Node):
    def __init__(self, variable: Token, expression: Node):
        if variable.token_type != TokenType.STRING:
            raise Exception("AssignNode: variable is not string")

        if not isinstance(expression, Node):
            raise Exception("AssignNode: expression is not Node")

        self.variable = variable
        self.expression = expression

    def execute(self):
        # TODO
        expression_value = self.expression.execute()
        return expression_value
