import pickle

import pandas as pd
import yfinance as yf
import data_classes.Agents as Agents
from TreeEnvironment import TreeEnv
from utils.fitness import simple_fitness, exponential_fitness, fitness_agent
from TreeEnvironment.TreeEvolution import TreeEvolution
from TreeEnvironment.TreeEnv import generate_random_tree


def main():
    tick1 = yf.Ticker("MSFT")
    data1 = tick1.history("1Y")

    tick2 = yf.Ticker("AAPL")
    data2 = tick2.history("1Y")

    tick3 = yf.Ticker("TGT")
    data3 = tick3.history("1Y")

    datasets = [data1, data2, data3]

    te = TreeEvolution()
    te.prepare_data(datasets)
    scores = TreeEnv.get_trees_scores(exponential_fitness, te.generation, datasets)
    print(scores.iloc[0].score)
    best_tree_id = scores.iloc[0].treeID.astype(int)
    best_tree = te.generation[best_tree_id]

    with open("best_tree", 'wb') as f:
        pickle.dump(best_tree, f)


# todo Create a class for transaction to make it for statistical analysis, logs
# todo Create mutate option for attribute mutation.


if __name__ == '__main__':
    main()
