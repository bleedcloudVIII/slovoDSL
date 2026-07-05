import numpy as np

from netopt.norm_folding.norm_folding import NormFolding
from netopt.enums import LayerType


def make_linear_weights(out_size=4, in_size=8):
    return {
        "fc1": {
            "weight": np.ones((out_size, in_size)),
            "bias": np.zeros(out_size)
        },
        "bn1": {
            "gamma": np.ones(out_size),
            "beta": np.zeros(out_size),
            "running_mean": np.zeros(out_size),
            "running_var": np.ones(out_size),
            "eps": 1e-5
        }
    }


def test_linear_bn_folding_removes_bn():
    structure = [
        {"name": "fc1",   "type": LayerType.Linear.value},
        {"name": "bn1",   "type": LayerType.BatchNorm.value},
        {"name": "relu1", "type": LayerType.ReLU.value},
    ]
    weights = make_linear_weights()

    new_structure, new_weights = NormFolding(structure, weights).execute()

    assert len(new_structure) == 2
    assert new_structure[0]["type"] == LayerType.Linear.value
    assert new_structure[1]["type"] == LayerType.ReLU.value
    assert "bn1" not in new_weights


def test_linear_bn_folding_updates_weights():
    structure = [
        {"name": "fc1", "type": LayerType.Linear.value},
        {"name": "bn1", "type": LayerType.BatchNorm.value},
    ]
    weights = make_linear_weights(out_size=4, in_size=8)

    _, new_weights = NormFolding(structure, weights).execute()

    assert new_weights["fc1"]["weight"].shape == (4, 8)
    assert new_weights["fc1"]["bias"].shape == (4,)


def test_linear_bn_folding_correct_math():
    structure = [
        {"name": "fc1", "type": LayerType.Linear.value},
        {"name": "bn1", "type": LayerType.BatchNorm.value},
    ]

    out_size = 2
    weights = {
        "fc1": {
            "weight": np.ones((out_size, 3)),
            "bias": np.zeros(out_size)
        },
        "bn1": {
            "gamma": np.array([2.0, 4.0]),
            "beta": np.array([1.0, 2.0]),
            "running_mean": np.array([0.0, 0.0]),
            "running_var": np.array([1.0, 1.0]),
            "eps": 0.0
        }
    }

    _, new_weights = NormFolding(structure, weights).execute()

    # scale = [2, 4]
    # W' = W * scale[:, None] = [[2,2,2], [4,4,4]]
    # b' = scale * (0 - 0) + beta = [1, 2]
    expected_weight = np.array([[2.0, 2.0, 2.0], [4.0, 4.0, 4.0]])
    expected_bias = np.array([1.0, 2.0])

    assert np.allclose(new_weights["fc1"]["weight"], expected_weight)
    assert np.allclose(new_weights["fc1"]["bias"], expected_bias)


def test_mixed_conv_linear_folding():
    structure = [
        {"name": "conv1", "type": LayerType.Conv2d.value},
        {"name": "bn1",   "type": LayerType.BatchNorm.value},
        {"name": "fc1",   "type": LayerType.Linear.value},
        {"name": "bn2",   "type": LayerType.BatchNorm.value},
    ]
    weights = {
        "conv1": {"weight": np.ones((4, 3, 3, 3)), "bias": np.zeros(4)},
        "bn1":   {
            "gamma": np.ones(4),
            "beta": np.zeros(4),
            "running_mean": np.zeros(4),
            "running_var": np.ones(4),
            "eps": 1e-5
        },
        "fc1":   {
            "weight": np.ones((8, 4)),
            "bias": np.zeros(8)
        },
        "bn2":   {
            "gamma": np.ones(8),
            "beta": np.zeros(8),
            "running_mean": np.zeros(8),
            "running_var": np.ones(8),
            "eps": 1e-5
        }
    }

    new_structure, new_weights = NormFolding(structure, weights).execute()

    assert len(new_structure) == 2
    assert "bn1" not in new_weights
    assert "bn2" not in new_weights
    assert "conv1" in new_weights
    assert "fc1" in new_weights
