import random
from anytree import Node, RenderTree


OPTIONAL_OUTPUTS = {
    0: "NOTHING",
    1: "BUY",
    2: "SELL"
}



class DecisionTreeAgent(object):
    def __init__(self, agents: list):
        random.shuffle(agents)
        
        self.agents = agents
        self.agent_id = {i: self.agents[i] for i in range(len(self.agents))}
        self._init_nodes() # Creates only the nodes.
        
        self.create_tree()
    
    def __repr__(self):
        print("Map of Agents")
        for key in self.agent_id.keys():
            print(key, "-->", self.agent_id[key].type)
        
        print()

        print(self.tree)
        return ""        
    def create_tree(self):
        self.root = self.nodes[0]
        
        for node in self.nodes[1:]:
            tmp_node = self.root
            branch = random.choice(range(len(tmp_node.children)))

            while type(tmp_node.children[branch].name) != str:
                tmp_node = tmp_node.children[branch]
                branch = random.choice(range(len(tmp_node.children)))
            
            tmp_children = list(tmp_node.children)
            tmp_children[branch] = node
            tmp_node.children = tmp_children
        
        self.tree = RenderTree(self.root)
                
    def _init_nodes(self):
        self.nodes = []
        
        for i in self.agent_id.keys():
            tmp_node = Node(i)
            self.add_none_children(tmp_node)
            self.nodes.append(tmp_node)
            
    def add_none_children(self, node):
        children = []
        
        for i in range(self.agent_id[node.name].n_outputs):
            outputs = random.choice(list(OPTIONAL_OUTPUTS.keys()))
            random_id = random.randint(1000, 9999)
            children.append(Node(str(outputs) + "-" + str(random_id)))
            
        node.children = children
    
    def run(self, data):
        tmp_node = self.root
        branch = self.agent_id[tmp_node.name].get_signal(data)
        
        while type(tmp_node.children[branch].name) == int:
            tmp_node = tmp_node.children[branch]
            branch = self.agent_id[tmp_node.name].get_signal(data)
        
        return int(tmp_node.children[branch].name.split("-")[0])

    def copy(self):
        return RenderTree(self.root)        

    
    
    
    