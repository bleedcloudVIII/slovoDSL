from compiler.ast.nodes.node import Node
from compiler.lexer.token import Token
from compiler.lexer.token_type import TokenType

# TODO Сделать хранение переменных нормальным
VARIABLES = {}


class AssignNode(Node):
    def __init__(self, variable: Token, expression: Node):
        if variable.token_type != TokenType.WORD:
            raise Exception("AssignNode: variable is not word")

        if not isinstance(expression, Node):
            raise Exception("AssignNode: expression is not Node")

        if variable.is_key_word:
            raise Exception("AssignNode: variable is a key word")

        self.variable_name = variable.token_text
        self.expression = expression

    def execute(self):
        expression_value = self.expression.execute()

        VARIABLES[self.variable_name] = expression_value

        return expression_value
