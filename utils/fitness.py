import pandas as pd
from typing import List, Dict
from pandas import DataFrame
from data_classes.Agents.Agent import Agent
from datetime import datetime


WINDOW = 30
N_STOCKS = 10
LOG_FOLDER = "logs\\"


def fitness_agent(fitness_func, agent: Agent, prepared_datasets: List[dict], tree_id: int, window=WINDOW,
                  n_stocks=N_STOCKS, log_transactions=False):
    amount = 0

    for row_data in prepared_datasets:
        amount += fitness_func(agent, row_data, tree_id, window, n_stocks, log_transactions=log_transactions)

    return amount


def simple_fitness(agent: Agent, row_data: dict, tree_id, window=WINDOW, n_stocks=N_STOCKS,
                   log_transactions=False):
    prepared_data = row_data["data"]
    symbol = row_data["symbol"]

    amount = 0
    is_invested = False

    if agent.n_outputs == 3:
        signal_mapper = {1: "BUY", 2: "SELL", 0: "NOTHING"}
    else:
        signal_mapper = {1: "BUY", 0: "SELL"}

    for i in range(window, len(prepared_data)):
        data_slice = prepared_data.iloc[i - window:i].copy()
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
        amount += prepared_data.iloc[-1]["Close"] * n_stocks

    return amount


def exponential_fitness(agent: Agent, row_data: pd.DataFrame, tree_id: int = 0, window=WINDOW, n_stocks=N_STOCKS,
                        log_transactions=False):
    prepared_data = row_data["data"]
    symbol = row_data["symbol"]

    first_amount = amount = 1000
    is_invested = False

    if agent.n_outputs == 3:
        signal_mapper = {1: "BUY", 2: "SELL", 0: "NOTHING"}
    else:
        signal_mapper = {1: "BUY", 0: "SELL"}

    n_stocks = 0

    points_of_transactions = []

    for i in range(window, len(prepared_data)):
        data_slice = prepared_data.iloc[i - window:i].copy()
        signal = signal_mapper[agent.get_signal(data_slice)]

        if signal == "BUY" and not is_invested:
            points_of_transactions.append(
                (
                    tree_id,
                    symbol,
                    "BUY",
                    data_slice.iloc[-1].Date,
                    data_slice.iloc[-1].Close
                )
            )
            current_stock_amount = data_slice.iloc[-1]["Close"]
            n_stocks = int(amount / current_stock_amount)
            amount -= current_stock_amount * n_stocks
            is_invested = True
        elif signal == "SELL" and is_invested:
            points_of_transactions.append(
                (
                    tree_id,
                    symbol,
                    "SELL",
                    data_slice.iloc[-1].Date,
                    data_slice.iloc[-1].Close
                )
            )
            current_stock_amount = data_slice.iloc[-1]["Close"]
            amount += current_stock_amount * n_stocks
            n_stocks = 0
            is_invested = False
        else:
            continue

    if is_invested:
        amount += prepared_data.iloc[-1]["Close"] * n_stocks

    if log_transactions:
        text = "TreeID,Symbol,Signal,Date,ClosePrice\n"
        text += "\n".join(
            [f"{tree_ident},{symbol},{signal},{date},{close}"
             for tree_ident, symbol, signal, date, close in points_of_transactions]
        )
        file_name = LOG_FOLDER + f"{symbol}_{datetime.now().strftime('%Y%m%d%H%M%S')}_{tree_id}.csv"

        with open(file_name, "w") as f:
            f.write(text)

    return amount - first_amount





