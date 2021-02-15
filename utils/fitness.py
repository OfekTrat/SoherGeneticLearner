from typing import List
from pandas import DataFrame
from data_classes.Agents.Agent import Agent


WINDOW = 30
N_STOCKS = 10


def fitness_agent(agent: Agent, datasets: List[DataFrame], window=WINDOW, n_stocks=N_STOCKS):
    amount = 0

    for data in datasets:
        amount += fitness_single_stock(agent, data, window, n_stocks)

    return amount


def fitness_single_stock(agent: Agent, data: DataFrame, window=WINDOW, n_stocks=N_STOCKS):
    data_copy = data.copy()
    agent.prepare_data(data_copy)
    amount = 0
    is_invested = False

    for i in range(window, len(data_copy)):
        data_slice = data_copy.iloc[i - window:i].copy()
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





