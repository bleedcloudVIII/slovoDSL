import numpy as np

from netopt.bn_folding.bn_folding import BNFolding
from netopt.enums import LayerType


def make_weights(out_ch=4, in_ch=3, kH=3, kW=3):
    return {
        "conv1": {
            "weight": np.ones((out_ch, in_ch, kH, kW)),
            "bias": np.zeros(out_ch)
        },
        "bn1": {
            "gamma": np.ones(out_ch),
            "beta": np.zeros(out_ch),
            "running_mean": np.zeros(out_ch),
            "running_var": np.ones(out_ch),
            "eps": 1e-5
        }
    }


def test_bn_folding_removes_bn():
    structure = [
        {"name": "conv1", "type": LayerType.Conv2d.value},
        {"name": "bn1",   "type": LayerType.BatchNorm.value},
        {"name": "relu1", "type": LayerType.ReLU.value},
    ]
    weights = make_weights()

    new_structure, new_weights = BNFolding(structure, weights).execute()

    assert len(new_structure) == 2
    assert new_structure[0]["type"] == LayerType.Conv2d.value
    assert new_structure[1]["type"] == LayerType.ReLU.value
    assert "bn1" not in new_weights


def test_bn_folding_updates_weights():
    structure = [
        {"name": "conv1", "type": LayerType.Conv2d.value},
        {"name": "bn1",   "type": LayerType.BatchNorm.value},
    ]
    weights = make_weights(out_ch=4)

    _, new_weights = BNFolding(structure, weights).execute()

    # gamma=1, mean=0, var=1, eps=1e-5 → scale ≈ 1
    # W' = W * 1 ≈ W
    assert new_weights["conv1"]["weight"].shape == (4, 3, 3, 3)
    assert new_weights["conv1"]["bias"].shape == (4,)


def test_bn_folding_correct_math():
    structure = [
        {"name": "conv1", "type": LayerType.Conv2d.value},
        {"name": "bn1",   "type": LayerType.BatchNorm.value},
    ]

    out_ch = 2
    weights = {
        "conv1": {
            "weight": np.ones((out_ch, 1, 1, 1)),
            "bias": np.zeros(out_ch)
        },
        "bn1": {
            "gamma": np.array([2.0, 4.0]),
            "beta": np.array([1.0, 2.0]),
            "running_mean": np.array([0.0, 0.0]),
            "running_var": np.array([1.0, 1.0]),
            "eps": 0.0
        }
    }

    _, new_weights = BNFolding(structure, weights).execute()

    # scale = gamma / sqrt(var) = [2, 4]
    # W' = W * scale = [2, 4]
    # b' = scale * (0 - 0) + beta = [1, 2]
    expected_weight = np.array([2.0, 4.0])
    expected_bias = np.array([1.0, 2.0])

    assert np.allclose(new_weights["conv1"]["weight"].flatten()[:2], expected_weight)
    assert np.allclose(new_weights["conv1"]["bias"], expected_bias)


def test_bn_folding_no_bn():
    structure = [
        {"name": "conv1", "type": LayerType.Conv2d.value},
        {"name": "relu1", "type": LayerType.ReLU.value},
    ]
    weights = make_weights()

    new_structure, new_weights = BNFolding(structure, weights).execute()

    assert len(new_structure) == 2
    assert "bn1" in new_weights


def test_bn_folding_multiple_blocks():
    structure = [
        {"name": "conv1", "type": LayerType.Conv2d.value},
        {"name": "bn1",   "type": LayerType.BatchNorm.value},
        {"name": "conv2", "type": LayerType.Conv2d.value},
        {"name": "bn2",   "type": LayerType.BatchNorm.value},
    ]
    weights = {
        "conv1": {"weight": np.ones((4, 3, 3, 3)), "bias": np.zeros(4)},
        "bn1":   {"gamma": np.ones(4), "beta": np.zeros(4), "running_mean": np.zeros(4), "running_var": np.ones(4), "eps": 1e-5},
        "conv2": {"weight": np.ones((8, 4, 3, 3)), "bias": np.zeros(8)},
        "bn2":   {"gamma": np.ones(8), "beta": np.zeros(8), "running_mean": np.zeros(8), "running_var": np.ones(8), "eps": 1e-5},
    }

    new_structure, new_weights = BNFolding(structure, weights).execute()

    assert len(new_structure) == 2
    assert "bn1" not in new_weights
    assert "bn2" not in new_weights
    assert "conv1" in new_weights
    assert "conv2" in new_weights