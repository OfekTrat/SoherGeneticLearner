from typing import List
from pandas import DataFrame
from data_classes.Agents.Agent import Agent


WINDOW = 30
N_STOCKS = 10


def fitness_agent(agent: Agent, prepared_datasets: List[DataFrame], window=WINDOW, n_stocks=N_STOCKS):
    amount = 0

    for data in prepared_datasets:
        amount += fitness_single_stock(agent, data, window, n_stocks)

    return amount


def fitness_single_stock(agent: Agent, prepared_data: DataFrame, window=WINDOW, n_stocks=N_STOCKS):
    data_copy = prepared_data.copy()
    amount = 0
    is_invested = False

    if agent.n_outputs == 3:
        signal_mapper = {1: "BUY", 2: "SELL", 0: "NOTHING"}
    else:
        signal_mapper = {1: "BUY", 0: "SELL"}

    for i in range(window, len(data_copy)):
        data_slice = data_copy.iloc[i - window:i].copy()
        signal = signal_mapper[agent.get_signal(data_slice)]

        if signal == "BUY" and not is_invested:
            amount -= data_slice.iloc[-1]["Close"] * n_stocks
            is_invested = True
        elif signal == "SELL" and is_invested:
            amount += data_slice.iloc[-1]["Close"] * n_stocks
            is_invested = False
        else:
            continue

    if is_invested:
        amount += data_slice.iloc[-1]["Close"] * n_stocks

    return amount





