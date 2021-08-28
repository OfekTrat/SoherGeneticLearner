from .Agent import Agent
import ta.trend as trend
import pandas as pd


class DPOAgent(Agent):
    def __init__(self, window=20):
        self.window = window
        self.column_name = f"dpo_{window}"
        self.n_outputs = 2

    def prepare_data(self, data: pd.DataFrame) -> pd.Series:
        dpo = trend.DPOIndicator(data["Close"], self.window)
        return dpo.dpo()

    def get_signal(self, prepared_data: pd.DataFrame) -> int:
        if prepared_data[self.column_name].iloc[-1] > 0:
            return 1  # PRICE ABOVE AVG
        else:
            return 0  # PRICE BELOW AVG

    def id(self) -> str:
        return self.column_name
