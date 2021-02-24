from .Agent import Agent
import ta.momentum as momentum
import pandas as pd



class TSIAgent(Agent):
    def __init__(self, slow_window=25, fast_window=13):
        self.slow_window = slow_window
        self.fast_window = fast_window

        self.column_name = f"tsi_{slow_window}_{fast_window}"

    def prepare_data(self, data):
        tsi = momentum.TSIIndicator(data["Close"], self.slow_window, self.fast_window)
        data[self.column_name] = tsi.tsi()

    def get_signal(self, prepared_data):
        if prepared_data[self.column_name].iloc[-1] > 0:
            return 1  # BUY
        else:
            return 0  # SELL

    def id(self):
        return self.column_name
