import configparser
from typing import List, Dict
import pandas as pd
from random import randint
from .tree_env import TreeEnv
from .tree_mutator import TreeMutator
from .tree_converger import TreeConverger
from .decision_tree import DecisionTree
from fitness.fitness_generation import FitnessGeneration
from fitness.ifitness import IFitness


class TreeEvolution(object):
    def __init__(self, n_trees: int, mutated_percentage: float,
                 converged_percentage: float, old_trees_percentage: float):
        self.n_trees = n_trees
        self.mutated_percentage = mutated_percentage
        self.converged_percentage = converged_percentage
        self.old_trees_percentage = old_trees_percentage
        self.generation = TreeEnv.generate_trees(n_trees)

    def prepare_data(self, data: Dict[str, pd.DataFrame]) -> Dict[str, pd.DataFrame]:
        all_trees = [tree for tree_id, tree in self.generation.items()]
        all_agents = set([(agent_name, agent) for tree in all_trees for agent_name, agent in tree.agents.items()])
        prepare_funcs = list()
        prepare_agents = list()

        for agent_name, agent in all_agents:
            if agent_name not in prepare_agents:
                prepare_funcs.append(agent.prepare_data)
                prepare_agents.append(agent_name)

        return {
            stock_name: pd.concat([func(table) for func in prepare_funcs] + [table["Close"]], axis=1)
            for stock_name, table in data.items()
        }

    def evolve(self, fitness_func: IFitness, prepared_datasets: Dict[str, pd.DataFrame],
               n_iterations: int) -> pd.DataFrame:
        scores = None

        for i in range(n_iterations):
            scores = self.__get_scores(fitness_func, prepared_datasets) \
                .sort_values("score", ascending=False, ignore_index=True)

            if self.__is_last_iteration(i, n_iterations):
                break

            self.__print_best_tree(scores, i)
            self.generation = self.__next_generation_by_score(scores)

        return scores

    def __get_scores(self, fitness_func: IFitness, prepared_datasets: Dict[str, pd.DataFrame]):
        return FitnessGeneration.run(fitness_func, self.generation, prepared_datasets)

    def __print_best_tree(self, scores: pd.DataFrame, iteration: int):
        print("Best Tree Amount:", scores.head(1)["score"].item(),
              "TreeID:", scores.head(1)["treeID"].item(),
              "Iteration:", iteration)

    def __is_last_iteration(self, i: int, n_iterations: int) -> bool:
        return (i + 1) == n_iterations

    def __next_generation_by_score(self, scores: pd.DataFrame):
        mutations = self.__get_mutations(scores)
        offsprings = self.__get_converged_trees(scores)
        old_trees = self.__get_old_trees(scores)
        new_trees = [TreeEnv.generate_random_tree()
                     for i in range(self.n_trees - len(mutations) - len(offsprings) - len(old_trees))]

        next_gen = mutations + offsprings + old_trees + new_trees
        next_gen = {tree_id: next_gen[tree_id] for tree_id in range(len(next_gen))}
        return next_gen

    def __get_mutations(self, tree_scores: pd.DataFrame) -> List[DecisionTree]:
        n_trees_to_mutate = int(self.n_trees * self.mutated_percentage)
        return [TreeMutator.mutate(self.__get_tree_by_chance(tree_scores)) for i in range(n_trees_to_mutate)]

    def __get_converged_trees(self, tree_scores: pd.DataFrame) -> List[DecisionTree]:
        n_trees_to_converge = int(self.n_trees * self.converged_percentage / 2)
        converged = [
            TreeConverger.converge(
                self.__get_tree_by_chance(tree_scores),
                self.__get_tree_by_chance(tree_scores)
            )
            for i in range(n_trees_to_converge)
        ]
        return [tree for tup in converged for tree in tup]

    def __get_old_trees(self, tree_scores: pd.DataFrame) -> List[DecisionTree]:
        n_old_trees = int(self.n_trees * self.old_trees_percentage)
        return [self.generation[tree_id] for tree_id in tree_scores["treeID"].head(n_old_trees)]

    def __get_tree_by_chance(self, tree_scores: pd.DataFrame) -> DecisionTree:
        chance = randint(int(tree_scores.score.min()), int(tree_scores.score.max()))
        tree_id = tree_scores.loc[tree_scores["score"] > chance].iloc[-1]["treeID"]
        return self.generation[tree_id]
