import configparser
from typing import List

import Tree.TreeEnv as TreeEnv
import pandas as pd

N_TREES = 150
MUTATED_PERCENTAGE = 0.2
CONVERGED_PERCENTAGE = 0.5
OLD_TREES_PERCENTAGE = 0.03


class TreeEvolution(object):
    def __init__(self, config_file=None):
        if config_file:
            self.load_file(config_file)
        else:
            self._init_defaults()

        self.generation = TreeEnv.create_gen(self.n_trees)

    def prepare_data(self, data: List[dict]):
        prepare_data_functions = {}

        for tree_id in self.generation.keys():
            for agent_id in self.generation[tree_id].agent_id.keys():
                if agent_id not in prepare_data_functions:
                    prepare_data_functions[agent_id] = self.generation[tree_id].agent_id[agent_id].prepare_data

        for row in data:
            dataset = row["data"]
            for func_id in prepare_data_functions.keys():
                prepare_data_functions[func_id](dataset)

    def evolve(self, fitness_func, prepared_datasets: List[dict], n_iterations, print_best=False,
               log_transactions=False) -> pd.DataFrame:
        scores = None

        for i in range(n_iterations):
            # Every iteration because the analyzing of the data changes overtime
            scores = TreeEnv.get_trees_scores(fitness_func, self.generation, prepared_datasets, log_transactions)

            if print_best:
                print("Best Tree Amount:", scores.head(1)["score"].item(),
                      "TreeID:", scores.head(1)["treeID"].item(),
                      "Iteration:", i)

            if (i + 1) != n_iterations:
                self.generation = self.next_generation_by_score(scores)

        return scores

    def next_generation_by_score(self, scores: pd.DataFrame):
        mutations = TreeEnv.mutate_gen(self.generation, scores, self.mutated_percentage)
        offsprings = TreeEnv.converged_gen(self.generation, scores, self.converged_percentage)
        old_trees = [self.generation[tree_id] for tree_id in scores["treeID"].head(int(self.n_trees * self.old_trees_percentage))]
        new_trees = [TreeEnv.generate_random_tree() for i in range(self.n_trees - len(mutations) - len(offsprings) - len(old_trees))]

        next_gen = mutations + offsprings + old_trees + new_trees
        next_gen = {tree_id: next_gen[tree_id] for tree_id in range(len(next_gen))}
        return next_gen

    def set_generation(self, generation):
        self.generation = generation

    def load_file(self, config_file):
        config = configparser.SafeConfigParser()
        config.read(config_file)
        self.n_trees = config.get("GENERATION", "N_TREES")
        self.n_iterations = config.get("EVOLUTION", "N_ITERATIONS")
        self.mutated_percentage = config.get("GENERATION", "MUTATED_PERCENTAGE")
        self.converged_percentage = config.get("GENERATION", "CONVERGED_PERCENTAGE")
        self.old_trees_percentage = config.get("GENERATION", "OLD_TREES_PERCENTAGE")

    def _init_defaults(self):
        self.n_trees = N_TREES
        self.mutated_percentage = MUTATED_PERCENTAGE
        self.converged_percentage = CONVERGED_PERCENTAGE
        self.old_trees_percentage = OLD_TREES_PERCENTAGE


