from netopt.enums import LayerType
from netopt.structure_opt.service import StructureOpt


def test_conv2d_relu_maxpooling():
    data = [
        {"type": LayerType.Conv2d.value},
        {"type": LayerType.ReLU.value},
        {"type": LayerType.MaxPooling.value},
    ]
    result = StructureOpt(data).execute()

    assert len(result) == 1
    assert result[0]["type"] == LayerType.Conv2d_ReLU_MaxPooling.value


def test_conv2d_relu_avgpooling():
    data = [
        {"type": LayerType.Conv2d.value},
        {"type": LayerType.ReLU.value},
        {"type": LayerType.AvgPooling.value},
    ]
    result = StructureOpt(data).execute()

    assert len(result) == 1
    assert result[0]["type"] == LayerType.Conv2d_ReLU_AvgPooling.value


def test_conv2d_maxpooling():
    data = [
        {"type": LayerType.Conv2d.value},
        {"type": LayerType.MaxPooling.value},
    ]
    result = StructureOpt(data).execute()

    assert len(result) == 1
    assert result[0]["type"] == LayerType.Conv2d_MaxPooling.value


def test_conv2d_avgpooling():
    data = [
        {"type": LayerType.Conv2d.value},
        {"type": LayerType.AvgPooling.value},
    ]
    result = StructureOpt(data).execute()

    assert len(result) == 1
    assert result[0]["type"] == LayerType.Conv2d_AvgPooling.value


def test_bn_folding_then_fusion():
    # Симулируем результат после BN Folding — BN исчез
    data = [
        {"type": LayerType.Conv2d.value},
        {"type": LayerType.ReLU.value},
        {"type": LayerType.MaxPooling.value},
    ]
    result = StructureOpt(data).execute()

    assert len(result) == 1
    assert result[0]["type"] == LayerType.Conv2d_ReLU_MaxPooling.value
