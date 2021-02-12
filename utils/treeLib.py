from copy import deepcopy
from random import randint, choice
from data_classes.DecisionTree.DecisionTreeAgent import DTA


TREE_CHOICES = ['0', '1', '2']


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
            if type(child.name) == int:  # Checks if the child is a node or an end branch
                queue.append(child)
            else:
                if count == chosen_leaf:
                    child.name = choice(TREE_CHOICES) + child.name[1:]
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

    # Changing the parents
    rand_node1.parent, rand_node2.parent = rand_node2.parent, rand_node1.parent

    # pruning the trees (removing duplicates)
    tree1_copy.prune_tree()
    tree2_copy.prune_tree()

    return tree1_copy, tree2_copy
