from enum import Enum


class FusionLayer(Enum):
    Conv2d_BatchNorm = "C2B"
    C2B_ReLU = "C2BR"
    Linear_BarchNorm = "LB"
    Linear_ReLU = "LR"
