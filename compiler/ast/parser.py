from compiler.common.token import Token
from compiler.common.token_type import TokenType
from compiler.ast.nodes.common_nodes.assign_node import AssignNode
from compiler.ast.nodes.common_nodes.bin_operator_node import BinOperatorTokenTypes, BinOperatorNode
from compiler.ast.nodes.common_nodes.number_node import NumberNode
from typing import List


class Parser():
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.line_position = 0
        self.nodes = []

        self._separate_lines()

    def _separate_lines(self):
        result = []
        current = []

        for t in self.tokens:
            if t.token_type == TokenType.NEW_LINE_SEPARATOR:
                if current:
                    result.append(current)
                    current = []
            else:
                current.append(t)

        if current:
            result.append(current)

        self.code_lines = result
        self.code_line_count = len(result)

    @property
    def current_token(self):
        return self.tokens[self.position]

    @property
    def current_token_type(self):
        return self.tokens[self.position].token_type

    def token(self, position: int):
        return self.tokens[position]

    def delta_token(self, delta: int):
        return self.tokens[self.position + delta]

    def parse_word_node(self, position: int = None):
        from compiler.ast.nodes.common_nodes.word_node import WordNode
        if position is None:
            position = self.position

        token = self.token(position)
        return WordNode(token)

    def parse_assign_node(self, position: int = None):
        if position is None:
            position = self.position

        variable = self.token(position - 1)
        value = self.token(position + 1)
        next_token = self.token(position + 2)

        if next_token.token_type in BinOperatorTokenTypes:
            value, delta = self.parse_bin_operator_node(position + 2)

        if variable.token_type == TokenType.WORD:
            variable = self.parse_word_node(position - 1)

        return (
            AssignNode(
                variable=variable,
                expression=value
            ),
            delta + 2
        )

    def parse_bin_operator_node(self, position: int = None):
        if position is None:
            position = self.position

        operator = self.token(position)

        if position + 1 > self.length:
            raise Exception("Parser: doesn't have all values")

        # TODO NumberNode а не Token
        left = self.token(position - 1)
        right = self.token(position + 1)

        if left.token_type in BinOperatorTokenTypes:
            left = self.parse_bin_operator_node(position - 1)

        if right.token_type in BinOperatorTokenTypes:
            right = self.parse_bin_operator_node(position + 1)

        if left.token_type == TokenType.NUMBER:
            left = NumberNode(left)

        if right.token_type == TokenType.NUMBER:
            right = NumberNode(right)

        return (
            BinOperatorNode(
                operator=operator,
                left_value=left,
                right_value=right
            ),
            2
        )

    def _parse_line(self, line_position: int = None):
        if line_position is None:
            line_position = self.line_position

        self.tokens = self.code_lines[line_position]

        self.position = 0
        self.length = len(self.tokens)

        while self.position < self.length:
            if self.current_token_type == TokenType.ASSIGN:
                node, delta = self.parse_assign_node()
                self.nodes.append(node)
                self.position += delta
            elif self.current_token_type == TokenType.WORD:
                # self.nodes.append(self.parse_word_node())
                self.position += 1
            elif self.current_token_type in BinOperatorTokenTypes:
                node, delta = self.parse_bin_operator_node()
                self.nodes.append(node)
                self.position += delta
            # else:
            #     self.position += 1

        # return self.nodes

    def parse(self):
        for i in range(self.code_line_count):
            self._parse_line(i)

        return self.nodes
