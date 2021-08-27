from .Agent import Agent
import pandas as pd
import ta.momentum as momentum


TREND_DIFF = 2

class KAMAAgent(Agent):
    def __init__(self, window=10, pow1=2, pow2=30):
        super().__init__()
        self.window = window
        self.pow1 = pow1
        self.pow2 = pow2

        self.column_name = f"kama_{window}_{pow1}_{pow2}"
        self.n_outputs = 3

    def prepare_data(self, data):
        kama = momentum.KAMAIndicator(data["Close"], self.window, self.pow1, self.pow2)
        data[self.column_name] = kama.kama()

    def get_signal(self, prepared_data):
        if prepared_data[self.column_name].iloc[-1] - \
                prepared_data[self.column_name].iloc[-1 * self.window] > TREND_DIFF:
            return 1  # TREND UP
        elif prepared_data[self.column_name].iloc[-1] - \
                prepared_data[self.column_name].iloc[-1 * self.window] < -1 * TREND_DIFF:
            return 2  # TREND DOWN
        else:
            return 0

    def id(self):
        return self.column_name


