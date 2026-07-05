# structure_opt/pipeline.py
from netopt.bn_folding.bn_folding import BNFolding
from netopt.bn_folding.weight_loader import WeightLoader
from netopt.structure_opt.service import StructureOpt
from netopt.identity_opt.service import IdentityOpt


class OptimizationPipeline:
    def __init__(self, structure: list):
        self.structure = structure

    def execute(self) -> list:
        # Этап 1 — удаляем Identity слои
        structure = IdentityOpt(self.structure).execute()

        # Этап 2 — весовые оптимизации (до fusion!)
        weights = {}
        if self.weights_path:
            weights = WeightLoader(self.weights_path).load()
            structure, weights = BNFolding(structure, weights).execute()

        # Этап 3 — структурные оптимизации (после BN Folding)
        structure = StructureOpt(structure).execute()

        return structure, weights
