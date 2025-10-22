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

    def _execute_miltiplication(self):
        left, right = self._get_int_values()

        return left * right

    def _execute_division(self):
        left, right = self._get_int_values()

        return left / right

    def _validate_values(self):
        # FIXME По идеи надо проверять, чтобы был один тип и возвращать его
        # И уже потом менять логику расчёта для каждого типа в _execute_ методах
        is_left_value_number = self.left_value.token_type == TokenType.NUMBER
        is_right_value_number = self.right_value.token_type == TokenType.NUMBER

        if is_left_value_number and is_right_value_number:
            return True

        raise Exception("BinOperatorNode: left or right not a number")

    def execute(self):
        self._validate_values()
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
