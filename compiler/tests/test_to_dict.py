from compiler.lexer.lexer import Lexer
from compiler.ast.parser import Parser
from compiler.ast.nodes.common_nodes.reverse_link_node import ReverseLinkNode


def parse(code: str):
    tokens = Lexer(code).lexer_analysis()
    return Parser(tokens).parse()


def to_structure(code: str):
    nodes = parse(code)
    return [node.to_dict() for node in nodes if isinstance(node, ReverseLinkNode)]


def test_dense_to_dict():
    structure = to_structure('a <- Dense(60)')
    assert len(structure) == 1
    assert structure[0]["name"] == "a"
    assert structure[0]["type"] == "Linear"
    assert structure[0]["input_size"] is not None
    assert structure[0]["dependency"] is None


def test_conv2d_to_dict():
    structure = to_structure('conv1 <- Conv2d({3, 3}; {1, 1}; {1, 1})')
    assert len(structure) == 1
    assert structure[0]["name"] == "conv1"
    assert structure[0]["type"] == "Conv2d"
    assert structure[0]["dependency"] is None


def test_batchnorm_to_dict():
    structure = to_structure('bn1 <- BatchNorm(10; 29; conv1)')
    assert len(structure) == 1
    assert structure[0]["name"] == "bn1"
    assert structure[0]["type"] == "BatchNorm"
    assert structure[0]["eps"] == 10
    assert structure[0]["momentum"] == 29
    assert structure[0]["dependency"] == "conv1"


def test_relu_to_dict():
    structure = to_structure('r <- ReLU(bn1)')
    assert len(structure) == 1
    assert structure[0]["name"] == "r"
    assert structure[0]["type"] == "ReLU"
    assert structure[0]["dependency"] == "bn1"


def test_dropout_to_dict():
    structure = to_structure('d <- Dropout(0.3; r)')
    assert len(structure) == 1
    assert structure[0]["name"] == "d"
    assert structure[0]["type"] == "Dropout"
    assert structure[0]["params"]["p"] is not None
    assert structure[0]["dependency"] == "r"


def test_add_to_dict():
    structure = to_structure('c <- Add({A, B})')
    assert len(structure) == 1
    assert structure[0]["name"] == "c"
    assert structure[0]["type"] == "Add"
    assert structure[0]["dependencies"] == ["A", "B"]


def test_concat_to_dict():
    structure = to_structure('c <- Concat({A, B}; 1)')
    assert len(structure) == 1
    assert structure[0]["name"] == "c"
    assert structure[0]["type"] == "Concat"
    assert structure[0]["axis"] == 1
    assert structure[0]["dependencies"] == ["A", "B"]


def test_maxpooling_to_dict():
    structure = to_structure('p <- MaxPooling(2)')
    assert len(structure) == 1
    assert structure[0]["name"] == "p"
    assert structure[0]["type"] == "MaxPooling"


def test_full_network_to_dict():
    code = """
    conv1 <- Conv2d({3, 3}; {1, 1}; {1, 1})
    bn1 <- BatchNorm(1; 1; conv1)
    relu1 <- ReLU(bn1)
    pool1 <- MaxPooling(2; relu1)
    fc1 <- Dense(128; sigmoid; pool1)
    """
    structure = to_structure(code)
    assert len(structure) == 5
    assert structure[0]["name"] == "conv1"
    assert structure[1]["name"] == "bn1"
    assert structure[1]["dependency"] == "conv1"
    assert structure[2]["name"] == "relu1"
    assert structure[2]["dependency"] == "bn1"
    assert structure[3]["name"] == "pool1"
    assert structure[4]["name"] == "fc1"
    assert structure[4]["dependency"] == "pool1"


def test_skip_connection_to_dict():
    code = """
    A <- Dense(5; softmax)
    B <- Dense(5; sigmoid; A)
    C <- Add({A, B})
    D <- Dense(10; relu; C)
    """
    structure = to_structure(code)
    assert len(structure) == 4
    assert structure[2]["name"] == "C"
    assert structure[2]["type"] == "Add"
    assert structure[2]["dependencies"] == ["A", "B"]
