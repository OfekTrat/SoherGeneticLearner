import pandas as pd
from random import choice, randint, random

# Agent importing
from data_classes.Agents.Agent import Agent
from data_classes.Agents.TrendAgent import TrendAgent
from data_classes.Agents.VolumeAgent import VolumeAgent
from data_classes.Agents.CandleStickAgent import CandleStickAgent
from data_classes.Agents.MovingAverageAgent import MACAgent
from data_classes.Agents.StochasticAgent import StochasticAgent
from data_classes.Agents.AverageDirectionalIndexAgent import ADXAgent

# Tree Importing
from data_classes.DecisionTree.DecisionTreeAgent import DTA

from utils.fitness import fitness_tree
from utils.treeLib import mutate_tree, converge_trees, rolling_score, get_tree_id_by_chance


MAC_SMALL_WINDOW = 5
MAC_LARGE_WINDOW = 20
VOL_SMALL_WINDOW = 3
VOL_LARGE_WINDOW = 14
STOCHASTIC_SMALL_WINDOW = 3
STOCHASTIC_LARGE_WINDOW = 14

NUM_OF_TREES = 100
N_ITERATIONS = 20

MUTATED_PERCENTAGE = 0.1
CONVERGED_PERCENTAGE = 0.8
STAYING_TREES_PERCENTAGE = 0.02


class TreeEnv(object):
    AGENT_TYPE = [TrendAgent, VolumeAgent, CandleStickAgent, MACAgent, StochasticAgent, ADXAgent]

    @classmethod
    def get_trees_score(cls, generation, data):
        score = [(tree, cls.fitness(generation[tree], data)) for tree in generation.keys()]
        return pd.DataFrame(score, columns=["treeID", "score"]).sort_values(by="score", ascending=False)

    @classmethod
    def _create_gen(cls):
        return {i: cls._generate_tree() for i in range(NUM_OF_TREES)}

    @classmethod
    def _generate_tree(cls):
        n_agents_in_tree = randint(1, len(cls.AGENT_TYPE) - 1)
        agents = [cls._generate_agent(choice(cls.AGENT_TYPE)) for i in range(n_agents_in_tree)]
        return DTA(agents)

    fitness = fitness_tree

    @staticmethod
    def _generate_agent(agent):
        agent_type = agent.TYPE

        if agent_type == "ADX":
            return agent()
        elif agent_type == "CandleStick":
            return agent()
        elif agent_type == "MACA":
            return agent(MAC_SMALL_WINDOW, MAC_LARGE_WINDOW)
        elif agent_type == "Stochastic":
            return agent(STOCHASTIC_SMALL_WINDOW, STOCHASTIC_LARGE_WINDOW)
        elif agent_type == "Trend":
            return agent()
        elif agent_type == "Volume":
            return agent(VOL_SMALL_WINDOW, VOL_LARGE_WINDOW)
        else:
            print("Cannot find agent")
            raise

    @classmethod
    def train(cls, data):
        generation = cls._create_gen()

        for i in range(N_ITERATIONS):
            score = rolling_score(cls.get_trees_score(generation, data))
            print("ITERATION:", (i+1), "BEST SCORE:", score.head(1)["score"])

            if (i + 1) != N_ITERATIONS:
                mutations = cls._mutate_gen(generation, score)
                converged_trees = cls._converged_gen(generation, score)
                old_trees = [generation[tree_id] \
                             for tree_id in score.head(int(len(score) * STAYING_TREES_PERCENTAGE))["treeID"]]
                new_trees = [cls._generate_tree() for i in range(len(generation) - len(converged_trees) \
                                                                 - len(mutations) - len(old_trees))]
                generation = mutations + converged_trees + new_trees
                generation = {i: generation[i] for i in range(len(generation))}

        return score, generation

    @classmethod
    def _mutate_gen(cls, generation, score_of_agents):
        n_trees_to_be_mutated = int(len(generation) * MUTATED_PERCENTAGE)
        mutations = []

        for i in range(n_trees_to_be_mutated):
            chance = random()
            tree_id = get_tree_id_by_chance(score_of_agents, chance)
            mutated_tree = mutate_tree(generation[tree_id])
            mutations.append(mutated_tree)

        return mutations

    @classmethod
    def _converged_gen(cls, generation, score_of_agents):
        n_converged_trees = int(len(generation) * CONVERGED_PERCENTAGE / 2)
        new_trees = []

        for i in range(n_converged_trees):
            chance1 = random()
            chance2 = random()

            tree_id1 = get_tree_id_by_chance(score_of_agents, chance1)
            tree_id2 = get_tree_id_by_chance(score_of_agents, chance2)

            tree1, tree2 = converge_trees(generation[tree_id1], generation[tree_id2])
            new_trees.append(tree1)
            new_trees.append(tree2)

        return new_trees
