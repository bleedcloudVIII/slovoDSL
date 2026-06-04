from enum import Enum


class LayerType(Enum):
    Conv2d = "Conv2d"
    ReLU = "ReLU"
    BatchNorm = "BatchNorm"
    Linear = "Lienar"

    # FusionLayer
    Conv2d_BatchNorm = "C2B"
    C2B_ReLU = "C2BR"
    Linear_BarchNorm = "LB"
    Linear_ReLU = "LR"
