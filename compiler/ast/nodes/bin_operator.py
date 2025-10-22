from compiler.ast.nodes.node import Node
from compiler.lexer.token import Token
from compiler.lexer.token_type import TokenType


class BinOperatorNode(Node):
    def __init__(self, operator: Token, left_value: Token, right_value: Token):
        self.operator = operator
        self.left_value = left_value
        self.right_value = right_value

    def _get_int_values(self):
        left_number = int(self.left_value.token_text)
        right_number = int(self.right_value.token_text)

        return left_number, right_number

    def _execute_plus(self):
        left, right = self._get_int_values()

        return left + right

    def _execute_minus(self):
        left, right = self._get_int_values()

        return left - right

    def _validate_values(self):
        is_left_value_number = self.left_value.token_type == TokenType.NUMBER
        is_right_value_number = self.right_value.token_type == TokenType.NUMBER

        if is_left_value_number and is_right_value_number:
            return True

        raise Exception("BinOperatorNode: left or right not a number")

    def execute(self):
        self._validate_values()

        if self.operator.token_type == TokenType.PLUS:
            return self._execute_plus()
        elif self.operator.token_type == TokenType.MINUS:
            return self._execute_minus()

        raise Exception(f"BinOperatorNode: operator {self.operator.token_type.name} is not supported")
