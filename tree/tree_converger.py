from anytree import Node
from copy import deepcopy
from typing import Tuple, Dict
from .decision_tree import DecisionTree
from random import randint
from .tree_pruner import TreePruner


class TreeConverger:
    @classmethod
    def converge(cls, tree1: DecisionTree, tree2: DecisionTree) -> Tuple[DecisionTree, DecisionTree]:
        tree1_copy = deepcopy(tree1)
        tree2_copy = deepcopy(tree2)

        overall_agents = cls.__converge_agents(tree1_copy, tree2_copy)
        tree1_copy.agents = overall_agents
        tree2_copy.agents = overall_agents

        random_node1 = cls.__get_random_node(tree1_copy)
        random_node2 = cls.__get_random_node(tree2_copy)

        print(random_node1, random_node2)

        if cls.__is_root(tree1_copy, random_node1):
            tree1_copy.root = random_node2
        if cls.__is_root(tree2_copy, random_node2):
            tree2_copy.root = random_node1

        random_node1.parent, random_node2.parent = random_node2.parent, random_node1.parent

        new_tree1 = TreePruner.prune(tree1_copy)
        new_tree2 = TreePruner.prune(tree2_copy)

        new_tree1.reset_nodes()
        new_tree2.reset_nodes()

        return new_tree1, new_tree2

    @staticmethod
    def __converge_agents(tree1: DecisionTree, tree2: DecisionTree) -> Dict:
        overall_dict = {}

        for key in tree1.agents.keys():
            overall_dict[key] = tree1.agents[key]

        for key in tree2.agents.keys():
            overall_dict[key] = tree2.agents[key]

        return overall_dict

    @staticmethod
    def __get_random_node(tree: DecisionTree) -> Node:
        rand_index = randint(0, tree.count_nodes() - 1)
        return tree.get_node(rand_index)

    @staticmethod
    def __is_root(tree, node) -> bool:
        return node is tree.root
