from .Agent import Agent
import pandas as pd
import ta.momentum as momentum


TREND_RANGE = 2


class ROCAgent(Agent):
    def __init__(self, window=12):
        super().__init__()
        self.window = window
        self.column_name = f"roc_{window}"
        self.n_outputs = 3

    def prepare_data(self, data):
        roc = momentum.ROCIndicator(data["Close"], self.window)
        data[self.column_name] = roc.roc()

    def get_signal(self, prepared_data):
        if prepared_data[self.column_name].iloc[-1] > TREND_RANGE:
            return 1  # TREND UP
        elif prepared_data[self.column_name].iloc[-1] < -1 * TREND_RANGE:
            return 2  # TREND DOWN
        else:
            return 0

    def id(self):
        return self.column_name