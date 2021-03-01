import pandas as pd
import yfinance as yf
import data_classes.Agents as Agents
from TreeEnvironment import TreeEnv
from utils.fitness import fitness_agent
from TreeEnvironment.TreeEvolution import TreeEvolution
from TreeEnvironment.TreeEnv import generate_random_tree


def main():
    tick1 = yf.Ticker("MSFT")
    data1 = tick1.history("1Y")

    tick2 = yf.Ticker("AAPL")
    data2 = tick2.history("1Y")

    # agent = Agents.MACAgent()
    # agent.prepare_data(data1)
    # agent.prepare_data(data2)
    # print(fitness_agent(agent, [data1, data2]))

    random_tree = generate_random_tree()
    random_tree.prepare_data(data1)
    random_tree.prepare_data(data2)
    print(fitness_agent(random_tree, [data1, data2]))



# todo Make converge and mutate functions not random (In the implementation of evolving, enter random values).

# todo Smarter fitness function
#       1. start with a certain amount
#       2. Buy as much as you can with the money


if __name__ == '__main__':
    main()
