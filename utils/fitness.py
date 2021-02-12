# import logging
from pandas import DataFrame
from data_classes.DecisionTree.DecisionTreeAgent import DTA

# logging.basicConfig(filename="c:\\users\ofeki\\desktop\\logs\\logger.txt", encoding="utf-8")
# logging.info("ACTION, STOCK_AMOUNT, N_STOCKS, CURRENT_AMOUNT")

WINDOW = 30
N_STOCKS = 10


def fitness_tree(tree: DTA, data: DataFrame, window=WINDOW, n_stocks=N_STOCKS):
    amount = 0
    is_invested = False

    for i in range(window, len(data)):
        data_slice = data.iloc[i-window:i].copy()
        signal = tree.run(data_slice)

        if signal == 1 and not is_invested:
            amount -= data_slice.iloc[-1]["Close"] * n_stocks
            is_invested = True
        elif signal == 2 and is_invested:
            amount += data_slice.iloc[-1]["Close"] * n_stocks
            is_invested = False
        else:
            continue

    if is_invested:
        amount += data_slice.iloc[-1]["Close"] * n_stocks

    return amount


def fitness_agent(agent, data, window=30, n_stocks=10):
    amount = 0
    is_invested = False

    for i in range(window, len(data)):
        data_slice = data.iloc[i - window:i].copy()
        signal = agent.get_signal(data_slice)

        if signal == 1 and not is_invested:
            amount -= data_slice.iloc[-1]["Close"] * n_stocks
            is_invested = True
        elif signal == 2 and is_invested:
            amount += data_slice.iloc[-1]["Close"] * n_stocks
            is_invested = False
        else:
            continue

    if is_invested:
        amount += data_slice.iloc[-1]["Close"] * n_stocks

    return amount




