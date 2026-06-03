from netopt.structure_opt.service import StructureOpt
from netopt.structure_opt.enums import FusionLayer


def test_conv2d_batch():
    json = [
        {
            "type": "Con2D"
        },
        {
            "type": "BatchNorm",
        }
    ]

    result = StructureOpt(json).execute()

    assert len(result) == 1
    assert result[0].get("type", "") == FusionLayer.Conv2d_BatchNorm.value


def test_conv2dbatch_relu():
    json = [
        {
            "type": "Con2D_BarchNorm"
        },
        {
            "type": "ReLU",
        }
    ]

    result = StructureOpt(json).execute()

    assert len(result) == 1
    assert result[0].get("type", "") == FusionLayer.C2B_ReLU.value


def test_linear_batch():
    json = [
        {
            "type": "Linear"
        },
        {
            "type": "BatchNorm",
        }
    ]

    result = StructureOpt(json).execute()

    assert len(result) == 1
    assert result[0].get("type", "") == FusionLayer.Linear_BarchNorm.value


def test_linear_relu():
    json = [
        {
            "type": "Linear"
        },
        {
            "type": "ReLU",
        }
    ]

    result = StructureOpt(json).execute()

    assert len(result) == 1
    assert result[0].get("type", "") == FusionLayer.Linear_ReLU.value
