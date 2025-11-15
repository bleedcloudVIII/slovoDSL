from compiler.ast.nodes.common_nodes.link_node import LINKS_OPERATORS_TOKEN_TYPE
from compiler.common.token import Token
from compiler.common.token_type import TokenType
from compiler.ast.nodes.common_nodes.assign_node import AssignNode
from compiler.ast.nodes.common_nodes.bin_operator_node import BIN_OPERATOR_TOKEN_TYPES, BinOperatorNode
from compiler.ast.nodes.common_nodes.number_node import NumberNode
from compiler.ast.nodes.common_nodes.link_node import LinkNode
from compiler.ast.nodes.common_nodes.reverse_link_node import ReverseLinkNode
from compiler.ast.nodes.common_nodes.path_node import PathNode
from compiler.ast.nodes.neuro_nodes.layer_node import LayerNode
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
    def current_token(self) -> Token:
        return self.tokens[self.position]

    @property
    def current_token_type(self) -> TokenType:
        return self.tokens[self.position].token_type

    @property
    def current_line_tokens(self) -> List[Token]:
        return self.code_lines[self.line_position]

    def token(self, position: int):
        return self.tokens[position]

    def delta_token(self, delta: int):
        return self.tokens[self.position + delta]

    def parse_word_node(self, position: int = None, token: Token = None):
        from compiler.ast.nodes.common_nodes.word_node import WordNode
        if position is None:
            position = self.position

        if token:
            return WordNode(token)

        token = self.token(position)
        return WordNode(token)

    def parse_assign_node(self, position: int = None):
        if position is None:
            position = self.position

        variable = self.token(position - 1)
        value = self.token(position + 1)
        next_token = self.token(position + 2)

        if next_token.token_type in BIN_OPERATOR_TOKEN_TYPES:
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
            raise Exception("Parser: doesn't have all values for BinOperatorNode")

        left = self.token(position - 1)
        right = self.token(position + 1)

        if left.token_type in BIN_OPERATOR_TOKEN_TYPES:
            left = self.parse_bin_operator_node(position - 1)

        if right.token_type in BIN_OPERATOR_TOKEN_TYPES:
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

    def _parse_link(self, left: Token, right: Token):
        # left - source
        # right - word | [] (layer)

        if left.token_type == TokenType.STRING:
            left = PathNode(left)
        elif left.token_type == TokenType.WORD:
            left = self.parse_word_node(token=left)

        if right.token_type == TokenType.WORD:
            right = self.parse_word_node(token=right)
        # TODO дописать, когда появится новая логика

        return (
            LinkNode(
                left=left,
                right=right
            ),
            2
        )

    def _parse_reverse_link(self, left: Token, right: Token):
        # right - word | []
        # right - source

        if right.token_type == TokenType.STRING:
            right = PathNode(right)
        elif right.token_type == TokenType.WORD:
            right = self.parse_word_node(token=right)

        if left.token_type == TokenType.WORD:
            left = self.parse_word_node(token=left)

        return (
            ReverseLinkNode(
                left=left,
                right=right
            ),
            2
        )

    def parse_link_operator_node(self, position: int = None):
        if position is None:
            position = self.position

        if position + 1 > self.length:
            raise Exception("Parser: doesn't have all values for LinkNode")

        operator = self.token(position)
        left = self.token(position - 1)
        right = self.token(position + 1)

        if operator.token_type == TokenType.LINK:
            return self._parse_link(left, right)
        elif operator.token_type == TokenType.REVERSE_LINK:
            return self._parse_reverse_link(left, right)
        else:
            raise Exception("Parser: Unknown operator_type in _parse_link_operator_node")

    def parse_layer_node(self, position: int = None):
        if position is None:
            position = self.position

        if position + 1 > self.length:
            raise Exception("Parser: doesn't have all values for LayerNode")

        if TokenType.LAYER_END not in [t.token_type for t in self.current_line_tokens]:
            raise Exception(f"Parser: layer doesn't closed at line {self.line_position + 1}")

        neurones_count = self.token(position + 1)

        if neurones_count.token_type == TokenType.LAYER_END:
            return (
                LayerNode(
                    neurons_count=None,
                    function=None
                ),
                2
            )
        # TODO обработка запятой
        if len(self.tokens) < 3:
            return (
                LayerNode(
                    neurons_count=NumberNode(neurones_count),
                    function=None
                ),
                4
            )

        func = self.token(position + 3)

        if func.token_type == TokenType.LAYER_END:
            return (
                LayerNode(
                    neurons_count=NumberNode(neurones_count),
                    function=None
                ),
                4
            )

        return (
            LayerNode(
                neurons_count=NumberNode(neurones_count),
                function=self.parse_word_node(token=func)
            ),
            5
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
                # TODO Смотреть следующий токен, если бинарный или линк пропускать, иначе ошибка?
                # self.nodes.append(self.parse_word_node())
                self.position += 1
            elif self.current_token_type in BIN_OPERATOR_TOKEN_TYPES:
                node, delta = self.parse_bin_operator_node()
                self.nodes.append(node)
                self.position += delta
            elif self.current_token_type in LINKS_OPERATORS_TOKEN_TYPE:
                node, delta = self.parse_link_operator_node()
                self.nodes.append(node)
                self.position += delta
            elif self.current_token.token_type == TokenType.LAYER_START:
                node, delta = self.parse_layer_node()
                self.nodes.append(node)
                self.position += delta
            else:
                self.position += 1

        # return self.nodes

    def parse(self):
        for i in range(self.code_line_count):
            self.line_position = i
            self.current_line_tokens
            self._parse_line(i)

        return self.nodes
