# structure_opt/pipeline.py
from netopt.structure_opt.service import StructureOpt
from netopt.identity_opt.service import IdentityOpt


class OptimizationPipeline:
    def __init__(self, structure: list):
        self.structure = structure

    def execute(self) -> list:
        structure = IdentityOpt(self.structure).execute()
        structure = StructureOpt(structure).execute()
        return structure
