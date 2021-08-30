from .decision_tree import DecisionTree
from anytree import Node
from typing import List
from copy import deepcopy


class TreePruner:
    @classmethod
    def prune(cls, tree: DecisionTree):
        tree_copy = deepcopy(tree)

        for node in tree_copy.iter_tree_nodes():
            for branch_num, child_node in enumerate(node.children):
                cls._prune_node(child_node, node.name, branch_num)

        return tree_copy

    @classmethod
    def _prune_node(cls, node, head_node_name, branch_value):
        current_name = node.name

        for child in node.children:
            if cls.__does_branch_continue(child):
                cls._prune_node(child, head_node_name, branch_value)

        if current_name == head_node_name:
            node.parent.children = cls.__change_parent_children(node, branch_value)

    @classmethod
    def __does_branch_continue(cls, child_node: Node) -> bool:
        return isinstance(child_node, str)

    @classmethod
    def __change_parent_children(cls, node: Node, branch: int) -> List[Node]:
        parent_node = node.parent
        child_to_replace = node.children[branch]
        parent_children = list(parent_node.children)

        node_index_as_child = parent_children.index(node)
        parent_children[node_index_as_child] = child_to_replace

        return parent_children
