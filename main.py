import copy
import pandas as pd
import yfinance as yf
from TreeEnvironment.TreeEvolution import TreeEvolution
from data_classes.Agents.MovingAverageAgent import MACAgent
from utils.fitness import fitness_agent
import pickle
from utils.stocksList import get_stock_list
from TreeEnvironment.TreeEnv import generate_random_tree, mutate_tree_node


def main():
    stock_list = get_stock_list(n_stocks=2)
    dataset = []

    for stock in stock_list:
        tick = yf.Ticker(stock)
        data = tick.history('1Y')
        dataset.append(data)

    te = TreeEvolution()
    scores = te.evolve(dataset, n_iterations=30, print_best=True)

    best_tree = te.generation[scores.head(1)["treeID"].item()]
    print(best_tree)












# todo implement mutations of agents that get parameters to initialize
# todo smarter fitness function
#       1. start with a certain amount
#       2. Buy as much as you can with the money


if __name__ == '__main__':
    main()
