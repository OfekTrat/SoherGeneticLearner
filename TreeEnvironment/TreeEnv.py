from typing import List, Dict

import pandas as pd
from copy import deepcopy
from random import choice, randint, random

# Agent importing
import data_classes.Agents as Agents

# Tree Importing
from data_classes.DecisionTree.DecisionTreeAgent import DTA
from utils.fitness import fitness_agent


MAC_SMALL_WINDOW = 5
MAC_LARGE_WINDOW = 20
VOL_SMALL_WINDOW = 3
VOL_LARGE_WINDOW = 14
STOCHASTIC_SMALL_WINDOW = 3
STOCHASTIC_LARGE_WINDOW = 14

TREE_CHOICES = [0, 1, 2]

AGENT_TYPES = [getattr(Agents, attribute) for attribute in dir(Agents) if not attribute.startswith("__")
               and attribute.endswith("Agent") and attribute != 'Agent']


def get_trees_scores(fitness_func, generation, prepared_datasets: Dict[str, pd.DataFrame], log_transactions=False):
    scores = [(tree, fitness_agent(fitness_func, generation[tree], prepared_datasets, tree, log_transactions=log_transactions))
              for tree in generation.keys()]
    scores = pd.DataFrame(scores, columns=["treeID", "score"]).sort_values(by="score", ascending=False)
    scores = rolling_chance(scores)
    return scores


def create_gen(n_trees):
    return {i: generate_random_tree() for i in range(n_trees)}


def generate_random_tree():
    n_agents_in_tree = randint(1, len(AGENT_TYPES) - 1)
    agents = [generate_random_agent(choice(AGENT_TYPES)) for i in range(n_agents_in_tree)]
    return DTA(agents)


def generate_random_agent(agent):
    return agent()


def mutate_gen(generation, score_of_agents, mutated_percentage):
    n_trees_to_be_mutated = int(len(generation) * mutated_percentage)
    mutations = []

    for i in range(n_trees_to_be_mutated):
        chance = random()
        tree_id = get_tree_id_by_chance(score_of_agents, chance)
        mutated_tree = mutate_tree(generation[tree_id])
        mutations.append(mutated_tree)

    return mutations


def converged_gen(generation, score_of_agents, converged_percentage):
    n_converged_trees = int(len(generation) * converged_percentage / 2)
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


def mutate_tree(tree_agent: DTA):
    tree_copy = deepcopy(tree_agent)

    # Choosing to mutate the nodes
    # if randint(0, 1) == 1:
    #     mutate_tree_node(tree_copy)

    number_of_leaves = tree_copy.count_leaves()
    chosen_leaf = randint(0, number_of_leaves - 1)

    count = 0

    for node in tree_copy.iter_tree():
        for child in node.children:
            if type(child.name) == int:
                if count == chosen_leaf:
                    child.name = choice(TREE_CHOICES)
                    break

                count += 1

    return tree_copy


def mutate_tree_node(tree: DTA):
    rand_node = choice(tree.nodes)
    random_agent = tree.agent_id[rand_node.name]

    if random_agent.MUTATED_ATTRS:
        rand_attr_to_change = choice(list(random_agent.MUTATED_ATTRS.keys()))
        range_of_change = random_agent.MUTATED_ATTRS[rand_attr_to_change]
        setattr(random_agent, rand_attr_to_change, randint(range_of_change[0], range_of_change[1]))
        rand_node.name = random_agent.id()
        tree.agent_id[random_agent.id()] = random_agent
    else:
        pass


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


def rolling_chance(score):
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
