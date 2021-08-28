from .Agent import Agent
import ta.trend as trend
import pandas as pd


class TRIXAgent(Agent):
    def __init__(self, window=15):
        self.window = window
        self.column_name = f"trix_{window}"
        self.n_outputs = 2

    def prepare_data(self, data: pd.DataFrame) -> pd.Series:
        trix = trend.TRIXIndicator(data["Close"], self.window)
        return trix.trix()

    def get_signal(self, prepared_data: pd.DataFrame) -> int:
        if prepared_data[self.column_name].iloc[-1] > 0:
            return 1  # BULL
        else:
            return 0  # BEAR

    def id(self) -> str:
        return self.column_name
