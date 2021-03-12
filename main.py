import pickle
import yfinance as yf
from TreeEnvironment import TreeEnv
from utils.fitness import exponential_fitness
from TreeEnvironment.TreeEvolution import TreeEvolution
from data_classes.DecisionTree import DecisionTreeAgent
import seaborn as sns
import matplotlib.pyplot as plt


def main():
    tick1 = yf.Ticker("MSFT")
    data1 = tick1.history("1Y")

    tick2 = yf.Ticker("AAPL")
    data2 = tick2.history("1Y")

    tick3 = yf.Ticker("TGT")
    data3 = tick3.history("1Y")

    datasets = [data1, data2, data3]

    tick4 = yf.Ticker("PM")
    data4 = tick4.history("2Y")

    with open("best_tree", "rb") as f:
        agent = pickle.load(f)

    agent.prepare_data(data4)
    amount = exponential_fitness(agent, data4)

    print(amount)

    # te = TreeEvolution()
    #
    # te.prepare_data(datasets)
    # scores = te.evolve(exponential_fitness, datasets, n_iterations=1, print_best=True)
    # best_tree_id = scores.iloc[0].treeID.astype(int)
    # print(f"Best Score:{scores.iloc[0].score}, Best Tree ID: {best_tree_id}")
    # print(f"Worst Score: {scores.iloc[-1].score}")
    # best_tree = te.generation[best_tree_id]

    # with open("best_tree", 'wb') as f:
    #     pickle.dump(best_tree, f)


# todo Create mutate option for attribute mutation.


if __name__ == '__main__':
    main()
