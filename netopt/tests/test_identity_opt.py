from netopt.identity_opt.service import IdentityOpt
from netopt.enums import LayerType


def test_dropout_zero_removed():
    data = [
        {"type": LayerType.Conv2d.value},
        {"type": LayerType.Dropout.value, "params": {"p": 0.0}},
        {"type": LayerType.ReLU.value},
    ]
    result = IdentityOpt(data).execute()

    assert len(result) == 2
    assert result[0]["type"] == LayerType.Conv2d.value
    assert result[1]["type"] == LayerType.ReLU.value


def test_dropout_nonzero_kept():
    data = [
        {"type": LayerType.Conv2d.value},
        {"type": LayerType.Dropout.value, "params": {"p": 0.5}},
    ]
    result = IdentityOpt(data).execute()

    assert len(result) == 1


def test_no_identity_layers():
    data = [
        {"type": LayerType.Conv2d.value},
        {"type": LayerType.BatchNorm.value},
        {"type": LayerType.ReLU.value},
    ]
    result = IdentityOpt(data).execute()

    assert len(result) == 3


def test_multiple_dropouts():
    data = [
        {"type": LayerType.Dropout.value, "params": {"p": 0.0}},
        {"type": LayerType.Linear.value},
        {"type": LayerType.Dropout.value, "params": {"p": 0.0}},
    ]
    result = IdentityOpt(data).execute()

    assert len(result) == 1
    assert result[0]["type"] == LayerType.Linear.value


def test_empty_structure():
    result = IdentityOpt([]).execute()
    assert result == []
