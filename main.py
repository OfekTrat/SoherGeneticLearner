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
    # agents = [getattr(Agents, agent)() for agent in dir(Agents) if agent.endswith("Agent") and agent != "Agent"]
    # stocks = pd.read_csv("all_stocks.csv")
    # data_folder = "data\\"
    #
    # for row in tqdm(stocks.itertuples()):
    #     start_date = datetime(2019, 1, 1)
    #     end_date = datetime.now()
    #     if row.symbol.endswith(".U"):
    #         tick = yf.Ticker(row.symbol[:-2])
    #         data = tick.history(interval="1d", start=start_date, end=end_date)
    #     else:
    #         tick = yf.Ticker(row.symbol)
    #         data = tick.history(interval="1d", start=start_date, end=end_date)
    #
    #     if len(data) < 100:
    #         continue
    #
    #     for agent in agents:
    #         agent.prepare_data(data)
    #
    #     start_date_str = start_date.strftime("%Y%m%d")
    #     end_date_str = end_date.strftime("%Y%m%d")
    #     fn = data_folder + f"{row.symbol}_{start_date_str}_{end_date_str}.csv"
    #



    #### SAMPLING DATA ####
    dirlist = [f"data\\{fn}" for fn in os.listdir("data") if fn != ".gitignore"]
    samples = choices(dirlist, k=5)

    datasets = []
    for sample in samples:
        fn_data = sample.split("\\")[1].split('.')[0].split("_")
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



    ###### CHECKING THE BEST BOT ######
    with open("best_tree", "rb") as f:
        best_tree = pickle.load(f)

    amount = 0
    for row in datasets:
        symbol = row["symbol"]
        data = row["data"]
        amount += exponential_fitness(best_tree, symbol, data, log_transactions=True)

    print(amount)

    ###### TRAINING THE BOTS ######
    # te = TreeEvolution()
    # scores = te.evolve(exponential_fitness, datasets, n_iterations=5, print_best=True)
    # best_tree_id = scores.iloc[0].treeID.astype(int)
    # print(f"Best Score:{scores.iloc[0].score}, Best Tree ID: {best_tree_id}")
    # print(f"Worst Score: {scores.iloc[-1].score}")
    # best_tree = te.generation[best_tree_id]

    ##### SAVING THE BEST BOT ######
    # with open("best_tree", 'wb') as f:
    #     pickle.dump(best_tree, f)


if __name__ == '__main__':
    main()

# todo Make datasets type: List[dict]
#  e.g. {"symbol": "MSFT", "start_date": datetime(2020, 1, 1), "end_date": datetime(2021, 1, 1), "prepared_data": pd.DataFrame}
#  this way i can know the symbol, time range (for better analyzation) and the data itself and not just symbol and data.
