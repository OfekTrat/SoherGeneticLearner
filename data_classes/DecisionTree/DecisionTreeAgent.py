from random import shuffle, choice, randint
from anytree import Node, RenderTree
from typing import List
from ..Agents.Agent import Agent

OPTIONAL_OUTPUTS = {
    0: "NOTHING",
    1: "BUY",
    2: "SELL"
}


class DTA(object):
    def __init__(self, agents: List[Agent]):
        shuffle(agents)
        self.agents = agents

        self.agent_id = {agent.id(): agent  for agent in self.agents}
        self._init_nodes()  # Creates only the nodes.
        self.root = self.nodes[0]
        self._create_tree()

    def __repr__(self):
        print(RenderTree(self.root))
        return ""

    def _create_tree(self):
        for node in self.nodes[1:]:
            tmp_node = self.root
            branch = choice(range(len(tmp_node.children)))

            while type(tmp_node.children[branch].name) == str:
                tmp_node = tmp_node.children[branch]
                branch = choice(range(len(tmp_node.children)))

            tmp_children = list(tmp_node.children)
            tmp_children[branch] = node
            tmp_node.children = tmp_children

    def _init_nodes(self):
        self.nodes = []

        for i in self.agent_id.keys():
            tmp_node = Node(i)
            self._add_none_children(tmp_node)
            self.nodes.append(tmp_node)

    def _add_none_children(self, node):
        children = []

        for i in range(self.agent_id[node.name].n_outputs):
            output = choice(list(OPTIONAL_OUTPUTS.keys()))
            children.append(Node(output))

        node.children = children

    def run(self, data):
        tmp_node = self.root
        branch = self.agent_id[tmp_node.name].get_signal(data)

        while type(tmp_node.children[branch].name) == str:
            tmp_node = tmp_node.children[branch]
            branch = self.agent_id[tmp_node.name].get_signal(data)

        return tmp_node.children[branch].name

    def copy(self):
        return RenderTree(self.root)

    def count_leaves(self):
        queue_nodes = []
        next_node = self.root
        queue_nodes.append(next_node)
        count = 0

        while True:
            for child in next_node.children:
                if type(child.name) == str:  # Checks if the child is a node or an end branch
                    queue_nodes.append(child)
                else:
                    count += 1

            queue_nodes = queue_nodes[1:]
            try:
                next_node = queue_nodes[0]
            except IndexError as e:
                return count

    def count_nodes(self):
        return len(self.nodes)

    def get_node(self, index):
        return self.nodes[index]

    def prune_tree(self):
        # Creating queue for pruning nodes
        next_node = self.root
        queue = [next_node]

        while True:
            for branch_value, child in enumerate(next_node.children):
                if type(child.name) == str:
                    self._prune_node(child, next_node.name, branch_value)
                    queue.append(child)

            queue = queue[1:]
            try:
                next_node = queue[0]
            except IndexError as e:
                break

    def _prune_node(self, node, node_id, branch_value):
        current_id = node.name
        for child in node.children:
            if type(child.name) == str:
                self._prune_node(child, node_id, branch_value)

        if current_id == node_id:
            parent_node = node.parent
            right_child = node.children[branch_value]
            parents_children = list(parent_node.children)
            nodes_index = parents_children.index(node)

            parents_children[nodes_index] = right_child
            parent_node.children = parents_children