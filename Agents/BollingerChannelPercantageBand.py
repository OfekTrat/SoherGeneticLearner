import pandas as pd
from .Agent import Agent
import ta.volatility as volatility


class BCPBAgent(Agent):
    def __init__(self, window=20, window_dev=2):
        self.window = window
        self.window_dev = window_dev
        self.column_name = f"bcpb_{window}_{window_dev}"
        self.n_outputs = 3

    def prepare_data(self, data: pd.DataFrame) -> pd.Series:
        bcpb = volatility.BollingerBands(data["Close"], self.window, self.window_dev)
        return bcpb.bollinger_pband()

    def get_signal(self, prepared_data: pd.DataFrame) -> int:
        if prepared_data[self.column_name].iloc[-1] > 0.8:
            return 1  # BUY
        elif prepared_data[self.column_name].iloc[-1] < 0.2:
            return 2  # SELL
        else:
            return 0

    def id(self) -> str:
        return self.column_name
