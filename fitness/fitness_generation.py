import pandas as pd
from typing import Dict
from .ifitness import IFitness
from tree.decision_tree import DecisionTree


class FitnessGeneration:
    @classmethod
    def run(cls, fitness_alg: IFitness, generation: Dict[int, DecisionTree],
            data: Dict[str, pd.DataFrame]) -> pd.DataFrame:
        results = []

        for tree_id, tree in generation.items():
            score = sum([fitness_alg.run(tree, stock_data) for stock_name, stock_data in data.items()])
            results.append({"treeID": tree_id, "score": score})

        return pd.DataFrame(results)

