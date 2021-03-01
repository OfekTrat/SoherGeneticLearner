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

    # agent = Agents.MACAgent()
    # agent.prepare_data(data1)
    # agent.prepare_data(data2)
    # print(fitness_agent(exponential_fitness, agent, [data1, data1]))
    # print(fitness_agent(simple_fitness, agent, [data1, data2]))

    # random_tree = generate_random_tree()
    # random_tree.prepare_data(data1)
    # random_tree.prepare_data(data2)
    # print(fitness_agent(exponential_fitness, random_tree, [data1, data2]))
    # print(fitness_agent(simple_fitness, random_tree, [data1, data2]))

    te = TreeEvolution()
    score = te.evolve(exponential_fitness, [data1, data2], 3, print_best=True)


# todo Create a class for transaction to make it for statistical analysis
# todo Create mutate option for attribute mutation.


if __name__ == '__main__':
    main()
