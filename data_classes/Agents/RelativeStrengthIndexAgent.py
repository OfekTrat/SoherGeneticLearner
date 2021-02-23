from .Agent import Agent
import pandas as pd
import ta.momentum as momentum


class RSIAgent(Agent):
    def __init__(self, window=14):
        self.window = window
        self.column_name = f"rsi_{window}"

    def prepare_data(self, data):
        rsi = momentum.RSIIndicator(data["Close"], self.window)
        data[self.column_name] = rsi.rsi()

    def get_signal(self, prepared_data):
        if prepared_data[self.column_name].iloc[-1] > 70:
            return 2  # SELL
        elif prepared_data[self.column_name].iloc[-1] < 30:
            return 1  # BUY
        else:
            return 0  # NOTHING

    def id(self):
        return self.column_name