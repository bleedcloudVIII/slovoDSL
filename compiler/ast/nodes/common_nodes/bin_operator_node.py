from compiler.ast.nodes.node import Node
from compiler.common.token import Token
from compiler.common.token_type import TokenType


BIN_OPERATOR_TOKEN_TYPES = [
    TokenType.PLUS,
    TokenType.MINUS,
    TokenType.MULTIPLICATION,
    TokenType.DIVISION
]


class BinOperatorNode(Node):
    def __init__(self, operator: Token, left_value: Node, right_value: Node):
        self.operator = operator
        self.left_value = left_value
        self.right_value = right_value

    def _execute_plus(self):
        left, right = self._get_values()

        return left + right

    def _execute_minus(self):
        left, right = self._get_values()

        return left - right

    def _get_values(self):
        left = self.left_value.execute()
        right = self.right_value.execute()

        return left, right

    def _execute_miltiplication(self):
        left, right = self._get_values()

        return left * right

    def _execute_division(self):
        left, right = self._get_values()

        return left / right

    def execute(self):
        token_type = self.operator.token_type

        if token_type == TokenType.PLUS:
            return self._execute_plus()
        elif token_type == TokenType.MINUS:
            return self._execute_minus()
        elif token_type == TokenType.MULTIPLICATION:
            return self._execute_miltiplication()
        elif token_type == TokenType.DIVISION:
            return self._execute_division()

        raise Exception(f"BinOperatorNode: operator {self.operator.token_type.name} is not supported")

    def __str__(self):
        return f"BinOperatorNode<{self.operator.token_type.name}, {self.left_value}, {self.right_value}>"

    def __repr__(self):
        return f"BinOperatorNode<{self.operator.token_type.name}, {self.left_value}, {self.right_value}>"
