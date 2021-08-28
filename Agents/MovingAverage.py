import pandas as pd
from .Agent import Agent
import ta.trend as trend


class MACAgent(Agent):
    def __init__(self, slow_window=26, fast_window=12):
        self.slow_window = slow_window
        self.fast_window = fast_window
        self.column_name = f"macd_{slow_window}_{fast_window}"
        self.n_outputs = 2

    def get_signal(self, prepared_data: pd.DataFrame) -> int:
        if prepared_data[self.column_name].iloc[-1] > 0:
            return 1  # BULL
        else:
            return 0  # BEAR

    def prepare_data(self, data: pd.DataFrame) -> pd.Series:
        macd = trend.MACD(data["Close"], self.slow_window, self.fast_window)
        return macd.macd_diff()

    def id(self) -> str:
        return self.column_name
