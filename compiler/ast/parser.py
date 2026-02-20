from compiler.common.token import Token
from compiler.common.token_type import TokenType
from compiler.ast.nodes.common_nodes.bin_operator_node import BIN_OPERATOR_TOKEN_TYPES, BinOperatorNode
from compiler.ast.nodes.common_nodes.number_node import NumberNode
from compiler.ast.nodes.common_nodes.link_node import LinkNode
from compiler.ast.nodes.common_nodes.reverse_link_node import ReverseLinkNode
from compiler.ast.nodes.common_nodes.path_node import PathNode
from compiler.ast.nodes.neuro_nodes.layer_node import LayerNode
from typing import List
from itertools import takewhile
from compiler.ast.nodes.common_nodes.word_node import WordNode
from compiler.ast.nodes.node import Node
from compiler.ast.nodes.common_nodes.list_node import ListNode
from compiler.ast.nodes.neuro_nodes.kernel_node import KernelNode
from utils.safe_get import safe_get


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

    def parse_word_node(self, token: Token = None) -> WordNode:
        """
        token = Token
        """
        if token:
            return WordNode(token)

    def parse_number_node(self, token: Token) -> NumberNode:
        """
        token = token
        """
        if token.token_type == TokenType.NUMBER:
            return NumberNode(token)

    def parse_bin_operator_node(self, left: Node, operator: Token, right: Node) -> BinOperatorNode:
        return BinOperatorNode(operator, left, right)

    def parse_bin_operator_expression(self, tokens: list[Token]) -> tuple[Node, int]:
        """
        tokens = [left_token, operator, right_tokens[]]
        """
        expression_tokens = list(takewhile(
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
            tokens
        ))

        # Ноды и токены
        token_types = [
            token.token_type
            if isinstance(token.token_type, Token)
            else token
            for token in expression_tokens
        ]

        token_index = 0
        delta = 0
        while token_index < len(token_types):
            token = token_types[token_index]
            if not isinstance(token, Token):
                token_index += 1
                continue

            if token.token_type == TokenType.MULTIPLICATION:
                left = token_types[token_index - 1]
                right = token_types[token_index + 1]
                operator = token_types[token_index]
                if isinstance(left, Token):
                    left = self.parse_number_node(left)

                if isinstance(right, Token):
                    right = self.parse_number_node(right)

                token_types.pop(token_index + 1)
                token_types.pop(token_index)
                token_types.pop(token_index - 1)
                token_types.insert(token_index - 1, self.parse_bin_operator_node(
                    left=left,
                    right=right,
                    operator=operator
                ))
                delta += 2
            elif token.token_type == TokenType.DIVISION:
                left = token_types[token_index - 1]
                right = token_types[token_index + 1]
                operator = token_types[token_index]
                if isinstance(left, Token):
                    left = self.parse_number_node(left)

                if isinstance(right, Token):
                    right = self.parse_number_node(right)

                token_types.pop(token_index + 1)
                token_types.pop(token_index)
                token_types.pop(token_index - 1)
                token_types.insert(token_index - 1, self.parse_bin_operator_node(
                    left=left,
                    right=right,
                    operator=operator
                ))
                delta += 2
            else:
                token_index += 1
                delta += 1

        token_index = 0
        while token_index < len(token_types):
            token = token_types[token_index]
            if not isinstance(token, Token):
                token_index += 1
                continue

            if token.token_type == TokenType.PLUS:
                left = token_types[token_index - 1]
                right = token_types[token_index + 1]
                operator = token_types[token_index]
                if isinstance(left, Token):
                    left = self.parse_number_node(left)

                if isinstance(right, Token):
                    right = self.parse_number_node(right)

                token_types.pop(token_index + 1)
                token_types.pop(token_index)
                token_types.pop(token_index - 1)
                token_types.insert(token_index - 1, self.parse_bin_operator_node(
                    left=left,
                    right=right,
                    operator=operator
                ))
                delta += 2
            elif token.token_type == TokenType.MINUS:
                left = token_types[token_index - 1]
                right = token_types[token_index + 1]
                operator = token_types[token_index]
                if isinstance(left, Token):
                    left = self.parse_number_node(left)

                if isinstance(right, Token):
                    right = self.parse_number_node(right)

                token_types.pop(token_index + 1)
                token_types.pop(token_index)
                token_types.pop(token_index - 1)
                token_types.insert(token_index - 1, self.parse_bin_operator_node(
                    left=left,
                    right=right,
                    operator=operator
                ))
                delta += 2
            else:
                token_index += 1
                delta += 1

        return (
            token_types[0],
            delta
        )

    def _parse_link(self, tokens: list[Token], operator_position: int) -> tuple[LinkNode, int]:
        left_tokens = tokens[:operator_position]
        right_tokens = tokens[operator_position + 1:]

        left_nodes, left_delta = self._parse_tokens(left_tokens)
        right_nodes, right_delta = self._parse_tokens(right_tokens)

        return (
            LinkNode(
                left=left_nodes[0],
                right=right_nodes[0]
            ),
            1 + right_delta + left_delta
        )

    def _parse_reverse_link(self, tokens: list[Token], operator_position: int) -> tuple[ReverseLinkNode, int]:
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

    def parse_layer_node(self, tokens: list[Token]) -> tuple[LayerNode, int]:
        """
        tokens = [layer_start, ..., layer_end]
        """
        expression_tokens = []
        current_expression_tokens = []
        for token in tokens:
            token_type = token.token_type
            if token_type == TokenType.LAYER_START:
                continue
            elif token_type in (TokenType.SEMICOLON, TokenType.LAYER_END):
                if current_expression_tokens:
                    expression_tokens.append(current_expression_tokens)
                    current_expression_tokens = []
            else:
                current_expression_tokens.append(token)
        if current_expression_tokens:
            expression_tokens.append(current_expression_tokens)

        expression_len = len(expression_tokens)

        delta = 0
        nodes = []

        for i in range(expression_len):
            node, node_delta = self._parse_tokens(expression_tokens[i])
            nodes.append(node[0])
            delta += node_delta

        # TODO Сделать проверку на тип для нод, чтобы понимать, что передаётся. Функция или всё таки базис

        return (
            LayerNode(
                neurons_count=safe_get(nodes, 0),
                function=safe_get(nodes, 1),
                bias=safe_get(nodes, 2)
            ),
            #          comma_count       + start_layer, end_layer
            delta + (expression_len - 1) + 2
        )

    def parse_list(self, tokens: List[Token]) -> tuple[ListNode, int]:
        expressions = []
        current_expression_tokens = []
        delta = 2
        for token in tokens:
            token_type = token.token_type
            if token_type == TokenType.LEFT_BRACE:
                continue
            elif token_type in (TokenType.COMMA, TokenType.RIGHT_BRACE, TokenType.NEW_LINE_SEPARATOR):
                if current_expression_tokens:
                    nodes, _delta = self._parse_tokens(current_expression_tokens)
                    if nodes and len(nodes) == 1:
                        expressions.append(nodes[0])
                    else:
                        expressions.append(nodes)
                    delta += _delta
                    current_expression_tokens = []
            else:
                delta += 1
                current_expression_tokens.append(token)
        if current_expression_tokens:
            nodes, _delta = self._parse_tokens(current_expression_tokens)
            if nodes and len(nodes) == 1:
                expressions.append(nodes[0])
            else:
                expressions.append(nodes)
            current_expression_tokens = []
            delta += _delta

        return (
            ListNode(expressions),
            delta
        )

    def parse_path(self, token: Token) -> tuple[PathNode, int]:
        return PathNode(path=token.token_text)

    def parse_kernel_node(self, tokens: list[Token]) -> tuple[LayerNode, int]:
        """
        tokens = [layer_start, ..., layer_end]
        """
        expression_tokens = []
        current_expression_tokens = []
        for token in tokens:
            token_type = token.token_type
            if token_type == TokenType.LEFT_PARENTHESES:
                continue
            elif token_type in (TokenType.SEMICOLON, TokenType.RIGHT_PARENTHESES):
                if current_expression_tokens:
                    expression_tokens.append(current_expression_tokens)
                    current_expression_tokens = []
            else:
                current_expression_tokens.append(token)
        if current_expression_tokens:
            expression_tokens.append(current_expression_tokens)

        expression_len = len(expression_tokens)

        delta = 0
        nodes = []

        for i in range(expression_len):
            node, node_delta = self._parse_tokens(expression_tokens[i])
            nodes.append(node[0])
            delta += node_delta

        # TODO Сделать проверку на тип для нод, чтобы понимать, что передаётся. Функция или всё таки базис

        return (
            KernelNode(
                columns=safe_get(nodes, 0),
                rows=safe_get(nodes, 1),
                function=safe_get(nodes, 2)
            ),
            #          comma_count       + start_layer, end_layer
            delta + (expression_len - 1) + 2
        )

    def _parse_tokens(self, tokens: List[Token] = None, position: int = None) -> tuple[list[Node], int]:
        position = 0 if position is None else position
        length = len(tokens)

        token_types = [token.token_type for token in tokens]

        nodes = []
        while position < length:
            current_token_type = tokens[position].token_type

            node = None
            delta = 0
            if TokenType.LINK in token_types:
                operator_position = token_types.index(TokenType.LINK)
                node, delta = self._parse_link(tokens, operator_position)
            elif TokenType.REVERSE_LINK in token_types:
                operator_position = token_types.index(TokenType.REVERSE_LINK)
                node, delta = self._parse_reverse_link(tokens, operator_position)
            elif current_token_type == TokenType.NUMBER:
                node = self.parse_number_node(tokens[position])
                delta += 1
            elif current_token_type == TokenType.WORD:
                node = self.parse_word_node(tokens[position])
                delta += 1
            elif current_token_type in BIN_OPERATOR_TOKEN_TYPES:
                nodes.pop()
                bin_operator_tokens = tokens[position - 1:]
                node, delta = self.parse_bin_operator_expression(bin_operator_tokens)
            elif current_token_type == TokenType.LAYER_START:
                layer_tokens = tokens[position:]
                node, delta = self.parse_layer_node(layer_tokens)
            elif current_token_type == TokenType.STRING:
                node = self.parse_path(tokens[position])
                delta = 1
            elif current_token_type == TokenType.LEFT_BRACE:
                list_tokens = tokens[position:]
                node, delta = self.parse_list(list_tokens)
            elif current_token_type == TokenType.LEFT_PARENTHESES:
                kernel_tokens = tokens[position:]
                node, delta = self.parse_kernel_node(kernel_tokens)
            else:
                position += 1
                continue

            if node is not None:
                nodes.append(node)
            position += delta

        return nodes, position

    def parse(self) -> list[Node]:
        nodes = []
        for i in range(self.code_line_count):
            tokens = self.line_tokens(i)
            new_nodes, _ = self._parse_tokens(tokens)
            nodes.extend(new_nodes)

        return nodes
