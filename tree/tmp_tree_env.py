import Agents
from random import choices, randint
from .decision_tree import DecisionTree
from typing import Dict


class TreeEnv:
    @classmethod
    def generate_trees(cls, n_trees: int) -> Dict[int, DecisionTree]:
        trees = {i: cls.generate_random_tree() for i in range(n_trees)}
        return trees

    @classmethod
    def generate_random_tree(cls) -> DecisionTree:
        agents = cls.__get_agent_list()
        random_number_of_agents = randint(1, len(agents) - 1)
        random_agents = choices(agents, k=random_number_of_agents)
        return DecisionTree(random_agents)

    @classmethod
    def __get_agent_list(cls):
        return [getattr(Agents, attribute)
                for attribute in dir(Agents) if not attribute.startswith("__")
                and attribute.endswith("Agent") and attribute != 'Agent']
