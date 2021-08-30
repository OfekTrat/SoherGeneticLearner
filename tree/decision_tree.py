from random import choice
from anytree import Node, RenderTree
from typing import List, Dict, Iterable
from agent_interfaces.isignaler import ISignaler
import pandas as pd

OPTIONAL_OUTPUTS = {
    0: "NOTHING",
    1: "BUY",
    2: "SELL"
}


class DecisionTree(ISignaler):
    def __init__(self, agents: List[ISignaler]):
        self.n_outputs = 3
        self.agents = self.__init_agents(agents)
        self.nodes = self.__init_nodes()
        self.root = self.nodes[0]
        self.__create_tree()

    def __init_agents(self, agents: List[ISignaler]) -> Dict[str, ISignaler]:
        return {agent().id(): agent() for agent in agents}

    def __init_nodes(self):
        nodes = []

        for agent_id in self.agents.keys():
            tmp_node = Node(agent_id)
            tmp_node.children = self.__generate_random_children(tmp_node)
            nodes.append(tmp_node)

        return nodes

    def __generate_random_children(self, node: Node) -> List[Node]:
        children = []

        for i in range(self.agents[node.name].n_outputs):
            output = choice(list(OPTIONAL_OUTPUTS.keys()))
            children.append(Node(output))

        return children

    def __create_tree(self):
        for node in self.nodes[1:]:
            self.__insert_node_as_offspring(node)

    def __insert_node_as_offspring(self, node: Node):
        head_node = self.root
        branch = choice(range(len(head_node.children)))

        while self.__has_child_in_branch(head_node, branch):
            head_node = head_node.children[branch]
            branch = choice(range(len(head_node.children)))

        tmp_children = list(head_node.children)
        tmp_children[branch] = node
        head_node.children = tmp_children

    @staticmethod
    def __has_child_in_branch(node: Node, branch: int) -> bool:
        return isinstance(node.children[branch].name, str)

    def iter_tree_nodes(self) -> Iterable[Node]:
        queue = list()
        next_node = self.root

        while True:
            for child in next_node.children:
                if self.__is_node_an_agent(child):
                    queue.append(child)

            yield next_node

            if not queue:
                break

            next_node = queue.pop(0)

    def get_signal(self, prepared_data: pd.DataFrame) -> int:
        head_node = self.root
        branch = self.agents[head_node.name].get_signal(prepared_data)

        while self.__has_child_in_branch(head_node, branch):
            head_node = head_node.children[branch]
            branch = self.agents[head_node.name].get_signal(prepared_data)

        return head_node.children[branch].name

    def prepare_data(self, data: pd.DataFrame) -> pd.DataFrame:
        all_columns = [agent.prepare_data(data).rename(agent_id) for agent_id, agent in self.agents.items()]
        prepared_data = pd.concat(all_columns + [data.Close], axis=1)

        return prepared_data

    def count_leaves(self) -> int:
        count = 0

        for node in self.iter_tree_nodes():
            for child in node.children:
                if not self.__is_node_an_agent(child):
                    count += 1

        return count

    def count_nodes(self) -> int:
        return len(list(self.iter_tree_nodes()))

    def get_node(self, index) -> Node:
        return self.nodes[index]

    def reset_nodes(self):
        self.nodes = list(self.iter_tree_nodes())

    @classmethod
    def __is_node_an_agent(cls, node) -> bool:
        return isinstance(node.name, str)

    def __repr__(self) -> str:
        print(RenderTree(self.root))
        return ""
