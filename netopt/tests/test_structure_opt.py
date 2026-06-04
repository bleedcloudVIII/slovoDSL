from netopt.structure_opt.service import StructureOpt
from netopt.enums import LayerType


def test_conv2d_batchnorm():
    data = [
        {"type": LayerType.Conv2d.value},
        {"type": LayerType.BatchNorm.value},
    ]
    result = StructureOpt(data).execute()

    assert len(result) == 1
    assert result[0]["type"] == LayerType.Conv2d_BatchNorm.value


def test_conv2d_relu():
    data = [
        {"type": LayerType.Conv2d.value},
        {"type": LayerType.ReLU.value},
    ]
    result = StructureOpt(data).execute()

    assert len(result) == 1
    assert result[0]["type"] == LayerType.Conv2d_ReLU.value


def test_conv2d_batchnorm_relu():
    data = [
        {"type": LayerType.Conv2d.value},
        {"type": LayerType.BatchNorm.value},
        {"type": LayerType.ReLU.value},
    ]
    result = StructureOpt(data).execute()

    assert len(result) == 1
    assert result[0]["type"] == LayerType.Conv2d_BatchNorm_ReLU.value


def test_linear_batchnorm():
    data = [
        {"type": LayerType.Linear.value},
        {"type": LayerType.BatchNorm.value},
    ]
    result = StructureOpt(data).execute()

    assert len(result) == 1
    assert result[0]["type"] == LayerType.Linear_BatchNorm.value


def test_linear_relu():
    data = [
        {"type": LayerType.Linear.value},
        {"type": LayerType.ReLU.value},
    ]
    result = StructureOpt(data).execute()

    assert len(result) == 1
    assert result[0]["type"] == LayerType.Linear_ReLU.value


def test_linear_batchnorm_relu():
    data = [
        {"type": LayerType.Linear.value},
        {"type": LayerType.BatchNorm.value},
        {"type": LayerType.ReLU.value},
    ]
    result = StructureOpt(data).execute()

    assert len(result) == 1
    assert result[0]["type"] == LayerType.Linear_BatchNorm_ReLU.value


def test_no_fusion():
    data = [
        {"type": LayerType.ReLU.value},
        {"type": LayerType.ReLU.value},
    ]
    result = StructureOpt(data).execute()

    assert len(result) == 2
    assert result[0]["type"] == LayerType.ReLU.value
    assert result[1]["type"] == LayerType.ReLU.value


def test_mixed_structure():
    data = [
        {"type": LayerType.Conv2d.value},
        {"type": LayerType.BatchNorm.value},
        {"type": LayerType.ReLU.value},
        {"type": LayerType.Linear.value},
        {"type": LayerType.ReLU.value},
    ]
    result = StructureOpt(data).execute()

    assert len(result) == 2
    assert result[0]["type"] == LayerType.Conv2d_BatchNorm_ReLU.value
    assert result[1]["type"] == LayerType.Linear_ReLU.value
