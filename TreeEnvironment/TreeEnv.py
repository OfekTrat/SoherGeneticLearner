import pandas as pd
from copy import deepcopy
from random import choice, randint, random

# Agent importing
from data_classes.Agents.TrendAgent import TrendAgent
from data_classes.Agents.VolumeAgent import VolumeAgent
from data_classes.Agents.CandleStickAgent import CandleStickAgent
from data_classes.Agents.MovingAverageAgent import MACAgent
from data_classes.Agents.StochasticAgent import StochasticAgent
from data_classes.Agents.AverageDirectionalIndexAgent import ADXAgent

# Tree Importing
from data_classes.DecisionTree.DecisionTreeAgent import DTA
from utils.fitness import fitness_agent


MAC_SMALL_WINDOW = 5
MAC_LARGE_WINDOW = 20
VOL_SMALL_WINDOW = 3
VOL_LARGE_WINDOW = 14
STOCHASTIC_SMALL_WINDOW = 3
STOCHASTIC_LARGE_WINDOW = 14

NUM_OF_TREES = 150
N_ITERATIONS = 20

MUTATED_PERCENTAGE = 0.2
CONVERGED_PERCENTAGE = 0.6
STAYING_TREES_PERCENTAGE = 0.03


AGENT_TYPE = [TrendAgent, VolumeAgent, CandleStickAgent, MACAgent, StochasticAgent, ADXAgent]


def get_trees_score(generation, data):
    score = [(tree, fitness_agent(generation[tree], data)) for tree in generation.keys()]
    return pd.DataFrame(score, columns=["treeID", "score"]).sort_values(by="score", ascending=False)


def _create_gen():
    return {i: _generate_random_tree() for i in range(NUM_OF_TREES)}


def _generate_random_tree():
    n_agents_in_tree = randint(1, len(AGENT_TYPE) - 1)
    agents = [_generate_random_agent(choice(AGENT_TYPE)) for i in range(n_agents_in_tree)]
    return DTA(agents)


def _generate_random_agent(agent):
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


def _mutate_gen(generation, score_of_agents):
    n_trees_to_be_mutated = int(len(generation) * MUTATED_PERCENTAGE)
    mutations = []

    for i in range(n_trees_to_be_mutated):
        chance = random()
        tree_id = get_tree_id_by_chance(score_of_agents, chance)
        mutated_tree = mutate_tree(generation[tree_id])
        mutations.append(mutated_tree)

    return mutations


def _converged_gen(generation, score_of_agents):
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




TREE_CHOICES = [0, 1, 2]


def mutate_tree(tree_agent: DTA):
    tree_copy = deepcopy(tree_agent)
    number_of_leaves = tree_copy.count_leaves()
    chosen_leaf = randint(0, number_of_leaves - 1)

    count = 0
    queue = []
    continue_iter = True
    tmp_node = tree_copy.root

    while continue_iter:
        for child in tmp_node.children:
            if type(child.name) == str:  # Checks if the child is a node or an end branch
                queue.append(child)
            else:
                if count == chosen_leaf:
                    child.name = choice(TREE_CHOICES)
                    continue_iter = False
                count += 1

        queue = queue[1:]
        try:
            tmp_node = queue[0]
        except IndexError as e:
            break

    return tree_copy


def _converge_dicts(dict1, dict2):
    overall_dict = {}

    for key in dict1.keys():
        overall_dict[key] = dict1[key]

    for key in dict2.keys():
        overall_dict[key] = dict2[key]

    return overall_dict


def converge_trees(tree1: DTA, tree2: DTA) -> tuple:
    agent_id1 = tree1.agent_id
    agent_id2 = tree2.agent_id
    overall_agents = _converge_dicts(agent_id2, agent_id1)

    # Coping Trees
    tree1_copy = deepcopy(tree1)
    tree2_copy = deepcopy(tree2)

    tree1_copy.agent_id = overall_agents
    tree2_copy.agent_id = overall_agents

    # Getting number of nodes
    count_nodes1 = tree1_copy.count_nodes()
    count_nodes2 = tree2_copy.count_nodes()

    # Getting random nodes
    rand_node1 = tree1_copy.get_node(randint(0, count_nodes1 - 1))
    rand_node2 = tree2_copy.get_node(randint(0, count_nodes2 - 1))

    if rand_node1 is tree1_copy.root:
        tree1_copy.root = rand_node2
    if rand_node2 is tree2_copy.root:
        tree2_copy.root = rand_node1

    # Changing the parents
    rand_node1.parent, rand_node2.parent = rand_node2.parent, rand_node1.parent

    # pruning the trees (removing duplicates)
    tree1_copy.prune_tree()
    tree2_copy.prune_tree()

    tree1_copy.reset_nodes()
    tree2_copy.reset_nodes()

    return tree1_copy, tree2_copy


def rolling_score(score):
    sum_score = (score["score"] - score["score"].min()).sum()
    score["Chance"] = (score["score"] - score["score"].min()) / sum_score
    score = score.sort_values(by="score", ignore_index=True)
    score["newChance"] = 0

    for i in range(len(score)):
        score.loc[i, "newChance"] = score.iloc[:i+1]["Chance"].sum()

    score["Chance"] = score["newChance"]
    score = score.drop(columns=["newChance"])
    return score.sort_values(by="score", ascending=False, ignore_index=True)


def get_tree_id_by_chance(score, chance):
    return int(score.loc[score["Chance"] > chance].iloc[-1]["treeID"])
