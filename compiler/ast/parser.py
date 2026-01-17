from compiler.common.token import Token
from compiler.common.token_type import TokenType
from compiler.ast.nodes.common_nodes.bin_operator_node import BIN_OPERATOR_TOKEN_TYPES, BinOperatorNode
from compiler.ast.nodes.common_nodes.number_node import NumberNode
from compiler.ast.nodes.common_nodes.link_node import LinkNode
from compiler.ast.nodes.common_nodes.reverse_link_node import ReverseLinkNode
# from compiler.ast.nodes.common_nodes.path_node import PathNode
from compiler.ast.nodes.neuro_nodes.layer_node import LayerNode
from typing import List
from itertools import takewhile
from compiler.ast.nodes.common_nodes.word_node import WordNode


class Parser():
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.code_lines = []
        self.code_line_count = 0

        self._separate_lines(tokens)

    def _separate_lines(self, tokens):
        result = []
        current = []

        for t in tokens:
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

    def line_tokens(self, line_position: int) -> List[Token]:
        return self.code_lines[line_position]

    def parse_word_node(self, token: Token = None):
        """
        token = Token
        """
        if token:
            return WordNode(token)

    def parse_number_node(self, token: Token):
        """
        token = token
        """
        if token.token_type == TokenType.NUMBER:
            return NumberNode(token)

    def parse_bin_operator_node(self, tokens: list[Token], position: int = None):
        """
        tokens = [left_token, operator, right_tokens[]]
        """
        operator = tokens[1]
        left_tokens = tokens[:1]
        right_tokens = list(takewhile(
            lambda token:
                token.token_type != TokenType.COMMA and
                token.token_type != TokenType.LAYER_END and
                token.token_type != TokenType.LINK and
                token.token_type != TokenType.REVERSE_LINK and
                token.token_type != TokenType.LAYER_START and
                token.token_type != TokenType.STRING and
                token.token_type != TokenType.WORD and
                token.token_type != TokenType.LEFT_BRACE and
                token.token_type != TokenType.LEFT_BRACKET and
                token.token_type != TokenType.LEFT_PARENTHESES and
                token.token_type != TokenType.RIGHT_BRACE and
                token.token_type != TokenType.RIGHT_BRACKET and
                token.token_type != TokenType.RIGHT_PARENTHESES,
            tokens[2:]
        ))

        left, left_position = self._parse_tokens(left_tokens)
        right, right_position = self._parse_tokens(right_tokens)

        left = left[-1]
        right = right[-1]

        return (
            BinOperatorNode(
                operator=operator,
                left_value=left,
                right_value=right
            ),
            1 + right_position
        )

    def _parse_link(self, tokens: list[Token], operator_position: int):
        left_tokens = tokens[:operator_position]
        right_tokens = tokens[operator_position + 1:]

        left_nodes, _ = self._parse_tokens(left_tokens)
        right_nodes, right_delta = self._parse_tokens(right_tokens)

        return (
            LinkNode(
                left=left_nodes[0],
                right=right_nodes[0]
            ),
            1 + right_delta
        )

    def _parse_reverse_link(self, tokens: list[Token], operator_position: int):
        left_tokens = tokens[:operator_position]
        right_tokens = tokens[operator_position + 1:]

        left_nodes, _ = self._parse_tokens(left_tokens)
        right_nodes, right_delta = self._parse_tokens(right_tokens)

        return (
            ReverseLinkNode(
                left=left_nodes[0],
                right=right_nodes[0]
            ),
            1 + right_delta
        )

    def parse_layer_node(self, tokens: list[Token]):
        """
        tokens = [layer_start, ..., layer_end]
        """
        neurones_count = tokens[1]

        if neurones_count.token_type == TokenType.LAYER_END:
            return (
                LayerNode(
                    neurons_count=None,
                    function=None
                ),
                2
            )

        if neurones_count.token_type == TokenType.COMMA:
            func = tokens[2]
            return (
                LayerNode(
                    neurons_count=None,
                    function=self.parse_word_node(func)
                ),
                1 + 2
            )

        # Берём все токены после LAYER_START и до COMMA и парсим
        neurons_tokens = list(takewhile(
            lambda token: token.token_type != TokenType.COMMA and token.token_type != TokenType.LAYER_END,
            tokens[1:]
        ))

        # Чтобы посчитать, сколько запятых в слое [...]
        layer_tokens = list(takewhile(
            lambda token: token.token_type != TokenType.LAYER_END,
            tokens[1:]
        ))

        comma_count = 0
        for token in layer_tokens:
            if token.token_type == TokenType.COMMA:
                comma_count += 1

        neurones_count, neurons_delta = self._parse_tokens(neurons_tokens)
        neurones_count = neurones_count[0]

        if comma_count < 1:
            return (
                LayerNode(
                    neurons_count=neurones_count,
                    function=None
                ),
                1 + neurons_delta
            )

        func = layer_tokens[-1]

        if func.token_type == TokenType.LAYER_END:
            return (
                LayerNode(
                    neurons_count=neurones_count,
                    function=None
                ),
                1 + neurons_delta
            )

        return (
            LayerNode(
                neurons_count=neurones_count,
                function=self.parse_word_node(token=func)
            ),
            # [   exp     ,  func  ]
            # ^   ^^^^^      ^^^^  ^
            # 1   delta   1     2  3
            1 + neurons_delta + 3
        )

    def _parse_tokens(self, tokens: List[Token] = None, position: int = None):
        position = 0 if position is None else position
        length = len(tokens)

        token_types = [token.token_type for token in tokens]

        nodes = []
        while position < length:
            current_token_type = tokens[position].token_type

            if TokenType.LINK in token_types:
                operator_position = token_types.index(TokenType.LINK)
                node, delta = self._parse_link(tokens, operator_position)
                nodes.append(node)
                position += delta
            elif TokenType.REVERSE_LINK in token_types:
                operator_position = token_types.index(TokenType.REVERSE_LINK)
                node, delta = self._parse_reverse_link(tokens, operator_position)
                nodes.append(node)
                position += delta
            elif current_token_type == TokenType.NUMBER:
                node = self.parse_number_node(tokens[position])
                nodes.append(node)
                position += 1
            elif current_token_type == TokenType.WORD:
                node = self.parse_word_node(tokens[position])
                nodes.append(node)
                position += 1
            elif current_token_type in BIN_OPERATOR_TOKEN_TYPES:
                nodes.pop()
                bin_operator_tokens = tokens[position - 1:]
                node, delta = self.parse_bin_operator_node(bin_operator_tokens)
                nodes.append(node)
                position += delta
            elif current_token_type == TokenType.LAYER_START:
                layer_tokens = tokens[position:]
                node, delta = self.parse_layer_node(layer_tokens)
                nodes.append(node)
                position += delta
            else:
                position += 1

        return nodes, position

    def parse(self):
        nodes = []
        for i in range(self.code_line_count):
            tokens = self.line_tokens(i)
            new_nodes, _ = self._parse_tokens(tokens)
            nodes.extend(new_nodes)

        return nodes
