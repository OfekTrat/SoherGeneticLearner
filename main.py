import copy
import pandas as pd
import yfinance as yf
from TreeEnvironment import TreeEnv
from data_classes.Agents.MovingAverageAgent import MACAgent
from utils.fitness import fitness_agent


def main():
    tick = yf.Ticker("MSFT")
    data = tick.history("1Y")


if __name__ == '__main__':
    main()

# todo create a treeEvolution object
# todo create a treeGeneration object??
# todo create a way to implement random initialization of an Agent
