from .Agent import Agent
import ta.trend as trend
import pandas as pd


class CCIAgent(Agent):
    def __init__(self, window=20):
        self.window = window
        self.column_name = f"cci_{window}"
        self.n_outputs = 3

    def prepare_data(self, data: pd.DataFrame) -> pd.Series:
        cci = trend.CCIIndicator(data["High"], data["Low"], data["Close"], self.window)
        return cci.cci()

    def get_signal(self, prepared_data: pd.DataFrame) -> int:
        if prepared_data[self.column_name].iloc[-1] > 100:
            return 2  # OVERBOUGHT
        elif prepared_data[self.column_name].iloc[-1] < -100:
            return 1  # OVERSOLD
        else:
            return 0

    def id(self) -> str:
        return self.column_name
