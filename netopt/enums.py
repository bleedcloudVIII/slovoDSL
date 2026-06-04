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

    # Fusion
    Conv2d_MaxPooling = "C2MP"
    Conv2d_AvgPooling = "C2AP"

    Conv2d_BatchNorm = "C2B"
    Conv2d_ReLU = "C2R"
    Conv2d_BatchNorm_ReLU = "C2BR"
    Conv2d_BatchNorm_ReLU_MaxPooling = "C2BRMP"
    Conv2d_BatchNorm_ReLU_AvgPooling = "C2BRAP"

    Linear_BatchNorm = "LB"
    Linear_ReLU = "LR"
    Linear_BatchNorm_ReLU = "LBR"
