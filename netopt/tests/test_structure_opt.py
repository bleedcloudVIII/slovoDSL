from netopt.structure_opt.service import StructureOpt
from netopt.structure_opt.enums import LayerType


def test_conv2d_batch():
    json = [
        {
            "type": LayerType.Conv2d.value
        },
        {
            "type": LayerType.BatchNorm.value,
        }
    ]

    result = StructureOpt(json).execute()

    assert len(result) == 1
    assert result[0].get("type", "") == LayerType.Conv2d_BatchNorm.value


def test_conv2dbatch_relu():
    json = [
        {
            "type": LayerType.Conv2d_BatchNorm.value
        },
        {
            "type": LayerType.ReLU.value,
        }
    ]

    result = StructureOpt(json).execute()

    assert len(result) == 1
    assert result[0].get("type", "") == LayerType.C2B_ReLU.value


def test_linear_batch():
    json = [
        {
            "type": LayerType.Linear.value
        },
        {
            "type": LayerType.BatchNorm.value,
        }
    ]

    result = StructureOpt(json).execute()

    assert len(result) == 1
    assert result[0].get("type", "") == LayerType.Linear_BarchNorm.value


def test_linear_relu():
    json = [
        {
            "type": LayerType.Linear.value
        },
        {
            "type": LayerType.ReLU.value,
        }
    ]

    result = StructureOpt(json).execute()

    assert len(result) == 1
    assert result[0].get("type", "") == LayerType.Linear_ReLU.value
