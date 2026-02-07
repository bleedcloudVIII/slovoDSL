from compiler.lexer.lexer import Lexer
from compiler.ast.parser import Parser
from compiler.ast.nodes.common_nodes.number_node import NumberNode
from compiler.ast.nodes.common_nodes.bin_operator_node import BinOperatorNode
from compiler.ast.nodes.common_nodes.word_node import WordNode
from compiler.ast.nodes.neuro_nodes.layer_node import LayerNode


def _get_tokens(code: str):
    return Lexer(code).lexer_analysis()


def test_number_parse():
    code = """ 60 """
    tokens = Lexer(code).lexer_analysis()

    assert len(tokens) == 1

    result = Parser(tokens).parse()
    assert len(result) == 1
    assert isinstance(result[0], NumberNode)
    assert result[0].token == tokens[0]


def test_word_parse():
    code = """ word """
    tokens = Lexer(code).lexer_analysis()

    assert len(tokens) == 1

    result = Parser(tokens).parse()
    assert len(result) == 1
    assert isinstance(result[0], WordNode)
    assert result[0].token == tokens[0]


def test_plus_parse():
    code = """ 60 + 20 """
    tokens = Lexer(code).lexer_analysis()

    assert len(tokens) == 3

    result = Parser(tokens).parse()
    assert len(result) == 1
    assert isinstance(result[0], BinOperatorNode)
    assert result[0].operator == tokens[1]
    assert isinstance(result[0].left_value, NumberNode)
    assert result[0].left_value.token == tokens[0]
    assert result[0].right_value.token == tokens[2]


def test_bin_operator_execute_1():
    code = """ 60 + 20 - 30 * 2 + 70 / 35 - 8 """
    tokens = Lexer(code).lexer_analysis()

    assert len(tokens) == 13

    result = Parser(tokens).parse()
    assert len(result) == 1
    assert result[0].execute() == 14


def test_bin_operator_execute_2():
    code = """ 60 + 90 - 20 / 10 * 3 """
    tokens = Lexer(code).lexer_analysis()

    assert len(tokens) == 9

    result = Parser(tokens).parse()
    assert len(result) == 1
    assert result[0].execute() == 144


def test_bin_operator_execute_3():
    code = """ 60 + 90 - 20 / 10 * 3 * 9 / 2 + 123 - 12313 """
    tokens = Lexer(code).lexer_analysis()

    assert len(tokens) == 17

    result = Parser(tokens).parse()
    assert len(result) == 1
    assert result[0].execute() == -12067


def test_bin_operator_execute_4():
    code = """ 60 / 90 - 13 * 3 / 2 - 20 / 10 * 3 * 9 / 2 """
    tokens = Lexer(code).lexer_analysis()

    assert len(tokens) == 19

    result = Parser(tokens).parse()
    assert len(result) == 1
    assert round(result[0].execute(), 5) == round(-45.83333, 5)


def test_empty_layer():
    code = """ [] """
    tokens = Lexer(code).lexer_analysis()

    assert len(tokens) == 2

    result = Parser(tokens).parse()
    assert len(result) == 1
    result = result[0]
    assert isinstance(result, LayerNode)
    assert result.neurons_count is None
    assert result.function is None
    assert result.bias is None


def test_layer_with_neurons():
    code = """ [80] """
    tokens = Lexer(code).lexer_analysis()

    assert len(tokens) == 3

    result = Parser(tokens).parse()
    assert len(result) == 1
    result = result[0]
    assert isinstance(result, LayerNode)
    assert isinstance(result.neurons_count, NumberNode)
    assert result.neurons_count.token.token_text == "80"
    assert result.function is None
    assert result.bias is None


def test_layer_with_neurons_and_func():
    code = """ [80, sigmoid] """
    tokens = Lexer(code).lexer_analysis()

    assert len(tokens) == 5

    result = Parser(tokens).parse()
    assert len(result) == 1
    result = result[0]
    assert isinstance(result, LayerNode)
    assert isinstance(result.neurons_count, NumberNode)
    assert result.neurons_count.token.token_text == "80"
    assert isinstance(result.function, WordNode)
    assert result.function.token.token_text == "sigmoid"
    assert result.bias is None


def test_layer_full():
    code = """ [80, sigmoid, bias_1] """
    tokens = Lexer(code).lexer_analysis()

    assert len(tokens) == 7

    result = Parser(tokens).parse()
    assert len(result) == 1
    result = result[0]
    assert isinstance(result, LayerNode)
    assert isinstance(result.neurons_count, NumberNode)
    assert result.neurons_count.token.token_text == "80"
    assert isinstance(result.function, WordNode)
    assert result.function.token.token_text == "sigmoid"
    assert isinstance(result.bias, WordNode)
    assert result.bias.token.token_text == "bias_1"
