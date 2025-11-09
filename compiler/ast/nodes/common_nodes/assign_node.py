from compiler.ast.nodes.node import Node
from compiler.common.token import Token
from compiler.common.token_type import TokenType

# TODO Сделать хранение переменных нормальным
VARIABLES = {}


class AssignNode(Node):
    def __init__(self, variable: Node, expression: Node):
        if not isinstance(expression, Node):
            raise Exception("AssignNode: expression is not Node")

        # if hasattr(variable, "is_key_word") and variable.is_key_word:
        if variable.is_key_word:
            raise Exception("AssignNode: variable is a key word")

        self.variable_name = variable.token.token_text
        self.expression = expression

    def execute(self):
        expression_value = self.expression.execute()

        VARIABLES[self.variable_name] = expression_value

        return expression_value

    def __str__(self):
        return f"AssignNode<{self.variable_name}, {self.expression}>"

    def __repr__(self):
        return f"AssignNode<{self.variable_name}, {self.expression}>"
