from typing import Optional, Tuple
import configparser
from .tree_evolution import TreeEvolution


class TreeEvolutionCreator:
    N_TREES = 10
    MUTATED_PERCENTAGE = 0.2
    CONVERGED_PERCENTAGE = 0.5
    OLD_TREES_PERCENTAGE = 0.1

    @classmethod
    def create(cls, config_file: Optional[str] = None) -> TreeEvolution:
        if config_file:
            parsed_args = cls.__parse(config_file)
            return TreeEvolution(*parsed_args)
        else:
            return TreeEvolution(cls.N_TREES, cls.MUTATED_PERCENTAGE,
                                 cls.CONVERGED_PERCENTAGE, cls.OLD_TREES_PERCENTAGE)

    @classmethod
    def __parse(cls, config_file: str) -> Tuple[int, float, float, float]:
        config = configparser.SafeConfigParser()
        config.read(config_file)
        n_trees = int(config.get("GENERATION", "N_TREES"))
        mutated_percentage = float(config.get("GENERATION", "MUTATED_PERCENTAGE"))
        converged_percentage = float(config.get("GENERATION", "CONVERGED_PERCENTAGE"))
        old_trees_percentage = float(config.get("GENERATION", "OLD_TREES_PERCENTAGE"))

        return n_trees, mutated_percentage, converged_percentage, old_trees_percentage
