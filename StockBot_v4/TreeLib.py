import random
import yfinance as yf
from Agents.Agent import Agent
from Agents.MovingAverageCrossoverAgent import MACAgent
from Agents.CandleStickAgent import CandleStickAgent
from Agents.AverageDirectionalIndexAgent import ADXAgent
from Agents.StochasticAgent import StochasticAgent
from Agents.TrendAgent import TrendAgent
from Agents.VolumeAgent import VolumeAgent
from DecisionTreeAgent import DecisionTreeAgent



def mutate(tree: DecisionTreeAgent) -> DecisionTreeAgent:
    copy = tree.copy()


def swap_nodes(tree1, tree2):
    copy1 = tree1.copy()
    copy2 = tree2.copy()


def main():
    mac = MACAgent(5, 20)
    cand = CandleStickAgent()
    adx = ADXAgent()
    stoch = StochasticAgent(14, 3)
    trend = TrendAgent()
    vol = VolumeAgent(3, 14)
    agents = [mac, cand, adx, stoch, trend, vol]
    
    tree1 =  DecisionTreeAgent(agents)
    tree2 = DecisionTreeAgent(agents)
    
    print(tree1)
    print()
    print()
    print(tree2)


if __name__ == '__main__':
    main()