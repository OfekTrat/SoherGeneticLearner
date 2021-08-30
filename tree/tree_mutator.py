from anytree import Node
from copy import deepcopy
from random import randint
from typing import Union, List
from .decision_tree import DecisionTree


class TreeMutator:
    @classmethod
    def mutate(cls, tree: DecisionTree) -> DecisionTree:
        tree_copy = deepcopy(tree)
        rand_leaf = cls.__choose_random_leaf(tree_copy)
        leaf = cls.__find_leaf(tree_copy, rand_leaf)
        leaf.name = randint(0, 2)
        return tree_copy

    @classmethod
    def __choose_random_leaf(cls, tree: DecisionTree) -> int:
        number_of_leaves = tree.count_leaves()
        return randint(0, number_of_leaves - 1)

    @classmethod
    def __find_leaf(cls, tree: DecisionTree, leaf_index: int) -> Node:
        count = 0

        for node in tree.iter_tree_nodes():
            for child_node in node.children:
                if cls.__is_child_leaf(child_node):
                    if count == leaf_index:
                        return child_node
                    else:
                        count += 1

    @classmethod
    def __is_child_leaf(cls, node: Node) -> bool:
        return isinstance(node.name, int)

