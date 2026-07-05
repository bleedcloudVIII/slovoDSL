import yaml
import numpy as np
from pathlib import Path


class WeightLoader:
    def __init__(self, path: str):
        self.path = Path(path)

    def load(self) -> dict:
        with open(self.path, "r") as f:
            config = yaml.safe_load(f)

        weights = {}
        for layer_name, layer_weights in config.get("weights", {}).items():
            weights[layer_name] = {}
            for key, file_path in layer_weights.items():
                weights[layer_name][key] = np.load(file_path)

        return weights