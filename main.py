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


DATA_FILE = "data"


def sample_data(n=5):
    dirlist = [f"{DATA_FILE}\\{fn}" for fn in os.listdir(DATA_FILE) if fn != ".gitignore"]
    samples = choices(dirlist, k=n)

    datasets = []
    for sample in samples:
        fn_data = sample.replace(".U", "").split("\\")[1].split('.')[0].split("_")
        symbol = fn_data[0]
        start_date = datetime.strptime(fn_data[1], "%Y%m%d")
        end_date = datetime.strptime(fn_data[2], "%Y%m%d")

        data = {
            "symbol": symbol,
            "start_date": start_date,
            "end_date": end_date,
            "data": pd.read_csv(sample)
        }
        datasets.append(data)

    return datasets


def data_collection():
    agents = [getattr(Agents, agent)() for agent in dir(Agents) if agent.endswith("Agent") and agent != "Agent"]
    stocks = pd.read_csv("all_stocks.csv")

    for row in tqdm(stocks.itertuples()):
        start_date = datetime(2019, 1, 1)
        end_date = datetime.now()
        if row.symbol.endswith(".U"):
            tick = yf.Ticker(row.symbol[:-2])
            data = tick.history(interval="1d", start=start_date, end=end_date)
        else:
            tick = yf.Ticker(row.symbol)
            data = tick.history(interval="1d", start=start_date, end=end_date)

        if len(data) < 100:
            continue

        for agent in agents:
            agent.prepare_data(data)

        start_date_str = start_date.strftime("%Y%m%d")
        end_date_str = end_date.strftime("%Y%m%d")
        fn = f"{DATA_FILE}\\{row.symbol}_{start_date_str}_{end_date_str}.csv"
        data.to_csv(fn)


def main():
    pass
    #### DATA COLLECTION ####
    # data_collection()


    ### SAMPLING DATA ####
    datasets = sample_data(500)


    ###### CHECKING THE BEST BOT ######
    # testing_stocks = ["data\\ETN_20190101_20210316.csv", "data\\ETN_20190101_20210316.csv"]
    # datasets = []
    # for fn in testing_stocks:
    #     fn_data = fn.split("\\")[1].split('.')[0].split("_")
    #     symbol = fn_data[0]
    #     start_date = datetime.strptime(fn_data[1], "%Y%m%d")
    #     end_date = datetime.strptime(fn_data[2], "%Y%m%d")
    #
    #     data = {
    #         "symbol": symbol,
    #         "start_date": start_date,
    #         "end_date": end_date,
    #         "data": pd.read_csv(fn)
    #     }
    #     datasets.append(data)
    #
    #
    # with open("best_tree", "rb") as f:
    #     best_tree = pickle.load(f)
    #
    # amount = 0
    # for row in datasets:
    #     amount += exponential_fitness(best_tree, row, log_transactions=True)
    #
    # print(amount)


    ###### TRAINING THE BOTS ######
    te = TreeEvolution()
    scores = te.evolve(exponential_fitness, datasets, n_iterations=150, print_best=True)
    best_tree_id = scores.iloc[0].treeID.astype(int)
    print()
    print(f"Best Score:{scores.iloc[0].score}, Best Tree ID: {best_tree_id}")
    print(f"Worst Score: {scores.iloc[-1].score}")
    best_tree = te.generation[best_tree_id]


    ##### SAVING THE BEST BOT ######
    with open("best_tree", 'wb') as f:
        pickle.dump(best_tree, f)


if __name__ == '__main__':
    main()
