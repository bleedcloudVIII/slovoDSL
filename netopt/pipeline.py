from netopt.identity_opt.service import IdentityOpt
from netopt.norm_folding.norm_folding import NormFolding
from netopt.norm_folding.weight_loader import WeightLoader
from netopt.pruning.weight_pruning import WeightPruning
from netopt.structure_opt.service import StructureOpt


class OptimizationPipeline:
    def __init__(self, structure: list, weights_path: str = None, pruning_threshold: float = None):
        self.structure = structure
        self.weights_path = weights_path
        self.pruning_threshold = pruning_threshold

    def execute(self) -> tuple[list, dict, dict]:
        structure = IdentityOpt(self.structure).execute()

        weights = {}
        pruning_report = {}
        if self.weights_path:
            weights = WeightLoader(self.weights_path).load()
            structure, weights = NormFolding(structure, weights).execute()

            if self.pruning_threshold is not None:
                structure, weights, pruning_report = WeightPruning(
                    structure, weights, self.pruning_threshold
                ).execute()

        structure = StructureOpt(structure).execute()

        return structure, weights, pruning_report
