import pandas as pd
from .Agent import Agent
import ta.momentum as momentum


AGENT_TYPE = "Stochastic"


class StochasticAgent(Agent):
    def __init__(self, window=14, smooth_window=3):
        self.n_outputs = 3
        self.window = window
        self.smooth = smooth_window
        self.column_name = f"stoch_{window}_{smooth_window}"
        self.n_outputs = 3

    def get_signal(self, prepared_data: pd.DataFrame) -> int:
        if prepared_data[self.column_name].iloc[-1] > 80:
            return 2  # SELL OVERBOUGHT
        elif prepared_data[self.column_name].iloc[-1] < 20:
            return 1  # BUY OVERSOLD
        else:
            return 0

    def prepare_data(self, data: pd.DataFrame) -> pd.Series:
        stochastic = momentum.StochasticOscillator(data["High"], data["Low"], data["Close"],
                                              self.window, self.smooth)

        return stochastic.stoch_signal()

    def id(self) -> str:
        return self.column_name

