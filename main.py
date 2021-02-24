import pandas as pd
import yfinance as yf
import data_classes.Agents as Agents


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
    tick = yf.Ticker("FB")
    data = tick.history("1Y")

    agent = Agents.MACAgent()
    # print(agent._get_int_attrs())


# todo 1. validate attributes: n_outputs, column_name
# todo 2. validate methods: id(), prepare_date(pd.DataFrame), get_signal(prepared_data)
# todo 3. validate inheritance: make sure super().__init__() is called

# todo Find tree implementation of json --- probably anytree is good enough for that.

# todo smarter fitness function
#       1. start with a certain amount
#       2. Buy as much as you can with the money


if __name__ == '__main__':
    main()
