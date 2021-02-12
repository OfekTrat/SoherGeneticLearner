from random import choice, randint

# Agent importing
from data_classes.Agents.Agent import Agent
from data_classes.Agents.TrendAgent import TrendAgent
from data_classes.Agents.VolumeAgent import VolumeAgent
from data_classes.Agents.CandleStickAgent import CandleStickAgent
from data_classes.Agents.MovingAverageAgent import MACAgent
from data_classes.Agents.StochasticAgent import StochasticAgent
from data_classes.Agents.AverageDirectionalIndexAgent import ADXAgent

# Tree Importing
from data_classes.DecisionTree.DecisionTreeAgent import DTA

from utils.fitness import fitness_tree


MAC_SMALL_WINDOW = 5
MAC_LARGE_WINDOW = 20
VOL_SMALL_WINDOW = 3
VOL_LARGE_WINDOW = 14
STOCHASTIC_SMALL_WINDOW = 3
STOCHASTIC_LARGE_WINDOW = 14

NUM_OF_TREES = 10
N_ITERATIONS = 20


class TreeEnv(object):
    AGENT_TYPE = [TrendAgent, VolumeAgent, CandleStickAgent, MACAgent, StochasticAgent, ADXAgent]

    def __init__(self):
        self._create_gen()

    def load_config(self, config_file):
        self.config = config_file

    def get_trees_score(self, data):
        score = {tree: TreeEnv.fitness(self.generation[tree], data) for tree in self.generation.keys()}
        return score

    def _create_gen(self):
        self.generation = {i: self._generate_tree() for i in range(NUM_OF_TREES)}

    @classmethod
    def _generate_tree(cls):
        n_agents_in_tree = randint(1, len(cls.AGENT_TYPE) - 1)
        agents = [cls._generate_agent(choice(cls.AGENT_TYPE)) for i in range(n_agents_in_tree)]
        return DTA(agents)

    fitness = fitness_tree

    @staticmethod
    def _generate_agent(agent):
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


