from enum import Enum


class LayerType(Enum):
    # Base layers
    Conv2d = "Conv2d"
    ReLU = "ReLU"
    BatchNorm = "BatchNorm"
    Linear = "Linear"
    Dropout = "Dropout"
    MaxPooling = "MaxPooling"
    AvgPooling = "AvgPooling"
    Add = "Add"
    Concat = "Concat"
    Input = "Input"

    # Fusion: Conv2d + BN (до BN Folding)
    Conv2d_BatchNorm = "C2B"
    Conv2d_BatchNorm_ReLU = "C2BR"
    Conv2d_BatchNorm_ReLU_MaxPooling = "C2BRMP"
    Conv2d_BatchNorm_ReLU_AvgPooling = "C2BRAP"

    # Fusion: Conv2d (после BN Folding — BN поглощён)
    Conv2d_ReLU = "C2R"
    Conv2d_ReLU_MaxPooling = "C2RMP"
    Conv2d_ReLU_AvgPooling = "C2RAP"
    Conv2d_MaxPooling = "C2MP"
    Conv2d_AvgPooling = "C2AP"

    # Fusion: Linear
    Linear_BatchNorm = "LB"
    Linear_ReLU = "LR"
    Linear_BatchNorm_ReLU = "LBR"
