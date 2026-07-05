import numpy as np

from netopt.enums import LayerType
from netopt.pruning.weight_pruning import WeightPruning


def test_conv_pruning_removes_zero_channels():
    structure = [
        {"name": "conv1", "type": LayerType.Conv2d.value},
        {"name": "conv2", "type": LayerType.Conv2d.value},
    ]
    weights = {
        "conv1": {
            "weight": np.array([
                np.ones((3, 3, 3)),    # канал 0 — норма > 0
                np.zeros((3, 3, 3)),   # канал 1 — норма = 0 → удаляем
                np.ones((3, 3, 3)),    # канал 2 — норма > 0
            ]),
            "bias": np.array([1.0, 0.0, 1.0])
        },
        "conv2": {
            "weight": np.ones((4, 3, 3, 3)),
            "bias": np.zeros(4)
        }
    }

    _, new_weights, report = WeightPruning(structure, weights, threshold=0.01).execute()

    assert new_weights["conv1"]["weight"].shape[0] == 2
    assert new_weights["conv1"]["bias"].shape[0] == 2
    assert new_weights["conv2"]["weight"].shape[1] == 2  # входы тоже уменьшились
    assert report["conv1"] == 1


def test_linear_pruning_removes_zero_neurons():
    structure = [
        {"name": "fc1", "type": LayerType.Linear.value},
        {"name": "fc2", "type": LayerType.Linear.value},
    ]
    weights = {
        "fc1": {
            "weight": np.array([
                [1.0, 2.0, 3.0],   # нейрон 0 — норма > 0
                [0.0, 0.0, 0.0],   # нейрон 1 — норма = 0 → удаляем
                [1.0, 1.0, 1.0],   # нейрон 2 — норма > 0
            ]),
            "bias": np.array([1.0, 0.0, 1.0])
        },
        "fc2": {
            "weight": np.ones((4, 3)),
            "bias": np.zeros(4)
        }
    }

    _, new_weights, report = WeightPruning(structure, weights, threshold=0.01).execute()

    assert new_weights["fc1"]["weight"].shape == (2, 3)
    assert new_weights["fc1"]["bias"].shape == (2,)
    assert new_weights["fc2"]["weight"].shape == (4, 2)  # входы уменьшились
    assert report["fc1"] == 1


def test_no_pruning_when_all_above_threshold():
    structure = [
        {"name": "fc1", "type": LayerType.Linear.value},
    ]
    weights = {
        "fc1": {
            "weight": np.ones((4, 3)),
            "bias": np.ones(4)
        }
    }

    _, new_weights, report = WeightPruning(structure, weights, threshold=0.01).execute()

    assert new_weights["fc1"]["weight"].shape == (4, 3)
    assert report["fc1"] == 0


def test_pruning_report():
    structure = [
        {"name": "fc1", "type": LayerType.Linear.value},
    ]
    weights = {
        "fc1": {
            "weight": np.array([
                [1.0, 2.0],
                [0.0, 0.0],
                [0.0, 0.0],
                [3.0, 4.0],
            ]),
            "bias": np.zeros(4)
        }
    }

    _, _, report = WeightPruning(structure, weights, threshold=0.01).execute()

    assert report["fc1"] == 2


def test_empty_structure():
    _, new_weights, report = WeightPruning([], {}, threshold=0.01).execute()
    assert new_weights == {}
    assert report == {}
