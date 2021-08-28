from .Agent import Agent
import pandas as pd
import ta.momentum as momentum


class ROCAgent(Agent):
    TREND_RANGE = 2

    def __init__(self, window=12):
        self.window = window
        self.column_name = f"roc_{window}"
        self.n_outputs = 3

    def prepare_data(self, data: pd.DataFrame) -> pd.Series:
        roc = momentum.ROCIndicator(data["Close"], self.window)
        return roc.roc()

    def get_signal(self, prepared_data: pd.DataFrame) -> int:
        if prepared_data[self.column_name].iloc[-1] > self.TREND_RANGE:
            return 1  # TREND UP
        elif prepared_data[self.column_name].iloc[-1] < -1 * self.TREND_RANGE:
            return 2  # TREND DOWN
        else:
            return 0

    def id(self) -> str:
        return self.column_name
