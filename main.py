import copy
import pandas as pd
import yfinance as yf
from TreeEnvironment.TreeEnv import TreeEnv
from data_classes.Agents.MovingAverageAgent import MACAgent
from utils.fitness import fitness_agent


def main():
    tick = yf.Ticker("MSFT")
    data = tick.history("1Y")

    # mac = MACAgent(5, 20)
    # mac.prepare_data(data)
    # print(fitness_agent(mac, data))
    tree = TreeEnv._generate_tree()
    print(tree)
    # te = TreeEnv()
    # score, generation = te.train(data)
    # print("ITERATION:", "LAST", "BEST SCORE:", score.head(1)["score"])


if __name__ == '__main__':
    main()
