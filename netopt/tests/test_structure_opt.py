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


def test_conv2d_batchnorm_relu_maxpooling():
    data = [
        {"type": LayerType.Conv2d.value},
        {"type": LayerType.BatchNorm.value},
        {"type": LayerType.ReLU.value},
        {"type": LayerType.MaxPooling.value},
    ]
    result = StructureOpt(data).execute()

    assert len(result) == 1
    assert result[0]["type"] == LayerType.Conv2d_BatchNorm_ReLU_MaxPooling.value


def test_conv2d_batchnorm_relu_avgpooling():
    data = [
        {"type": LayerType.Conv2d.value},
        {"type": LayerType.BatchNorm.value},
        {"type": LayerType.ReLU.value},
        {"type": LayerType.AvgPooling.value},
    ]
    result = StructureOpt(data).execute()

    assert len(result) == 1
    assert result[0]["type"] == LayerType.Conv2d_BatchNorm_ReLU_AvgPooling.value


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


def test_pooling_without_conv_not_fused():
    data = [
        {"type": LayerType.MaxPooling.value},
        {"type": LayerType.ReLU.value},
    ]
    result = StructureOpt(data).execute()

    assert len(result) == 2
    assert result[0]["type"] == LayerType.MaxPooling.value
    assert result[1]["type"] == LayerType.ReLU.value


def test_mixed_structure():
    data = [
        {"type": LayerType.Conv2d.value},
        {"type": LayerType.BatchNorm.value},
        {"type": LayerType.ReLU.value},
        {"type": LayerType.MaxPooling.value},
        {"type": LayerType.Linear.value},
        {"type": LayerType.ReLU.value},
    ]
    result = StructureOpt(data).execute()

    assert len(result) == 2
    assert result[0]["type"] == LayerType.Conv2d_BatchNorm_ReLU_MaxPooling.value
    assert result[1]["type"] == LayerType.Linear_ReLU.value


def test_empty_structure():
    result = StructureOpt([]).execute()
    assert result == []


def test_add_breaks_fusion():
    data = [
        {"type": LayerType.Conv2d.value},
        {"type": LayerType.Add.value},
        {"type": LayerType.BatchNorm.value},
        {"type": LayerType.ReLU.value},
    ]
    result = StructureOpt(data).execute()

    assert len(result) == 4
    assert result[0]["type"] == LayerType.Conv2d.value
    assert result[1]["type"] == LayerType.Add.value
    assert result[2]["type"] == LayerType.BatchNorm.value
    assert result[3]["type"] == LayerType.ReLU.value


def test_concat_breaks_fusion():
    data = [
        {"type": LayerType.Conv2d.value},
        {"type": LayerType.Concat.value},
        {"type": LayerType.BatchNorm.value},
        {"type": LayerType.ReLU.value},
    ]
    result = StructureOpt(data).execute()

    assert len(result) == 4
    assert result[0]["type"] == LayerType.Conv2d.value
    assert result[1]["type"] == LayerType.Concat.value
    assert result[2]["type"] == LayerType.BatchNorm.value
    assert result[3]["type"] == LayerType.ReLU.value