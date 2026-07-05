from compiler.lexer.lexer import Lexer
from compiler.ast.parser import Parser
from compiler.ast.nodes.neuro_nodes.add_node import AddNode
from compiler.ast.nodes.neuro_nodes.concat_node import ConcatNode
from compiler.ast.nodes.common_nodes.reverse_link_node import ReverseLinkNode


def parse(code: str):
    tokens = Lexer(code).lexer_analysis()
    return Parser(tokens).parse()


def test_add_simple():
    nodes = parse('c <- Add({A, B})')
    assert len(nodes) == 1
    assert isinstance(nodes[0], ReverseLinkNode)
    assert isinstance(nodes[0].right, AddNode)
    assert nodes[0].right.dependencies is not None
    assert len(nodes[0].right.dependencies.expressions) == 2


def test_add_to_dict():
    nodes = parse('c <- Add({A, B})')
    result = nodes[0].right.to_dict()
    assert result["type"] == "Add"
    assert "dependencies" in result
    assert len(result["dependencies"]) == 2


def test_concat_default_axis():
    nodes = parse('c <- Concat({A, B})')
    assert isinstance(nodes[0].right, ConcatNode)
    assert nodes[0].right.axis.execute() == 1
    result = nodes[0].right.to_dict()
    assert result["axis"] == 1


def test_concat_custom_axis():
    nodes = parse('c <- Concat({A, B}; 0)')
    assert isinstance(nodes[0].right, ConcatNode)
    result = nodes[0].right.to_dict()
    assert result["axis"] == 0


def test_concat_three_inputs():
    nodes = parse('c <- Concat({A, B, C}; 2)')
    concat = nodes[0].right
    assert isinstance(concat, ConcatNode)
    assert len(concat.dependencies.expressions) == 3
    assert concat.to_dict()["axis"] == 2


def test_add_in_network():
    code = """
    A <- Dense(5; softmax)
    B <- Dense(5; sigmoid; {A})
    C <- Add({A, B})
    D <- Dense(10; relu; {C})
    """
    nodes = parse(code)
    assert len(nodes) == 4
    assert isinstance(nodes[2].right, AddNode)


def test_concat_in_network():
    code = """
    A <- Conv2d({3, 3})
    B <- Conv2d({3, 3})
    C <- Concat({A, B}; 1)
    D <- Dense(10; {C})
    """
    nodes = parse(code)
    assert len(nodes) == 4
    assert isinstance(nodes[2].right, ConcatNode)
    assert nodes[2].right.to_dict()["axis"] == 1
