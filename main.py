import pickle
import pandas as pd
import yfinance as yf
from TreeEnvironment import TreeEnv
from utils.fitness import exponential_fitness
from TreeEnvironment.TreeEvolution import TreeEvolution
from data_classes.DecisionTree import DecisionTreeAgent
from utils.stocksList import get_stock_list
from data_classes import Agents
from datetime import datetime
from tqdm import tqdm
import os
from random import choices


def main():
    #### DATA COLLECTION ####
    agents = [getattr(Agents, agent)() for agent in dir(Agents) if agent.endswith("Agent") and agent != "Agent"]
    stocks = pd.read_csv("all_stocks.csv")
    data_folder = "data\\"

    for row in tqdm(stocks.itertuples()):
        if row.symbol.endswith(".U"):
            tick = yf.Ticker(row.symbol[:-2])
            data = tick.history(interval="1d", start=datetime(2019, 1, 1), end=datetime.now())
        else:
            tick = yf.Ticker(row.symbol)
            data = tick.history(interval="1d", start=datetime(2019, 1, 1), end=datetime.now())

        if len(data) < 100:
            continue

        for agent in agents:
            agent.prepare_data(data)

        fn = data_folder + f"{row.symbol}.csv"
        data.to_csv(fn)


    #### SAMPLING DATA ####
    # dirlist = [f"data\\{fn}" for fn in os.listdir("data")]
    # samples = choices(dirlist, k=5)
    #
    # datasets = {}
    # for sample in samples:
    #     symbol = sample.split("\\")[1].split(".")[0]
    #     datasets[symbol] = pd.read_csv(sample)


    ###### CHECKING THE BEST BOT ######
    # with open("best_tree", "rb") as f:
    #     best_tree = pickle.load(f)
    #
    # for symbol, data in datasets.items():
    #     best_tree.prepare_data(data)
    #     exponential_fitness(best_tree, symbol, data, log_transactions=True)

    ###### TRAINING THE BOTS ######
    te = TreeEvolution()
    scores = te.evolve(exponential_fitness, datasets, n_iterations=5, print_best=True)
    best_tree_id = scores.iloc[0].treeID.astype(int)
    print(f"Best Score:{scores.iloc[0].score}, Best Tree ID: {best_tree_id}")
    print(f"Worst Score: {scores.iloc[-1].score}")
    best_tree = te.generation[best_tree_id]

    ##### SAVING THE BEST BOT ######
    # with open("best_tree", 'wb') as f:
    #     pickle.dump(best_tree, f)


if __name__ == '__main__':
    main()
