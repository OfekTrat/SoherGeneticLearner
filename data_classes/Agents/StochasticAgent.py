import pandas as pd
from .Agent import Agent
import ta.momentum as momentum


AGENT_TYPE = "Stochastic"


class StochasticAgent(Agent):
    TYPE = AGENT_TYPE
    MUTATED_ATTRS = {"k_window_size": (10, 20), "d_window_size": (1,7)}

    def __init__(self, window=14, smooth_window=3):
        super().__init__(AGENT_TYPE)
        self.n_outputs = 3
        self.window = window
        self.smooth = smooth_window

        self.column_name = f"stoch_{window}_{smooth_window}"

    def get_signal(self, prepared_data):
        if prepared_data[self.column_name].iloc[-1] > 80:
            return 2  # SELL OVERBOUGHT
        elif prepared_data[self.column_name].iloc[-1] < 20:
            return 1  # BUY OVERSOLD
        else:
            return 0

    def prepare_data(self, data):
        stochastic = momentum.StochasticOscillator(data["High"], data["Low"], data["Close"],
                                              self.window, self.smooth)

        data[self.column_name] = stochastic.stoch_signal()

    def id(self):
        return self.column_name

