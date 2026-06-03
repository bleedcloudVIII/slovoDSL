
Conv2d
BatchNorm
Conv2d (fused)
BN впечён в веса


Conv2d + BN
(уже слиты)
ReLU
Conv-BN-ReLU
1 CUDA-ядро


Linear
BatchNorm1d
Linear (fused)
bias поглощает BN


Linear
ReLU / GELU
активация
Linear+act (fused)
меньше записей в RAM


Depthwise Conv
по каналам отдельно
Pointwise Conv
1×1, mix каналов
MobileNet-блок
в разы меньше FLOP


MultiheadAttention
Out projection
Fused Attention
меньше матр. умножений