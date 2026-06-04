from enum import Enum


class LayerType(Enum):
    # Base layers
    Conv2d = "Conv2d"
    ReLU = "ReLU"
    BatchNorm = "BatchNorm"
    Linear = "Linear"
    Dropout = "Dropout"

    # Fusion: Conv2d
    Conv2d_BatchNorm = "C2B"
    Conv2d_ReLU = "C2R"
    Conv2d_BatchNorm_ReLU = "C2BR"

    # Fusion: Linear
    Linear_BatchNorm = "LB"
    Linear_ReLU = "LR"
    Linear_BatchNorm_ReLU = "LBR"
