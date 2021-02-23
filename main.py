import pandas as pd
import yfinance as yf
from data_classes.Agents.MassIndexAgent import MIAgent
import ta.volume as volume
import matplotlib.pyplot as plt

def main():
    # stock_list = get_stock_list(n_stocks=2)
    # dataset = []
    #
    # for stock in stock_list:
    #     tick = yf.Ticker(stock)
    #     data = tick.history('1Y')
    #     dataset.append(data)
    #
    # te = TreeEvolution()
    # scores = te.evolve(dataset, n_iterations=30, print_best=True)
    #
    # best_tree = te.generation[scores.head(1)["treeID"].item()]
    # print(best_tree)
    tick = yf.Ticker("AAPL")
    data = tick.history("1Y")

    agent = MIAgent()
    agent.prepare_data(data)
    plt.plot(data[agent.id()].values)
    plt.show()




# todo STOPPED AT: Trend Indicators

# todo think about changing buying signals to trend signals (do not tell when to buy or sell but when a tred is up or
#  down)

# todo READ ALL THE FUNCTIONALITIES OF ta MODULE AND IMPLEMNT AGENTS OF THEM - USE THE TA DOCUMENTATION AND
#  INVESTOPEDIA FOR UNDERSTAING THE INDICATORS
# todo validate new Agents that they have all of the attributes needed, default attribues, parameters matching documentation
# todo change most agents to use ta module
# todo smarter fitness function
#       1. start with a certain amount
#       2. Buy as much as you can with the money


if __name__ == '__main__':
    main()
