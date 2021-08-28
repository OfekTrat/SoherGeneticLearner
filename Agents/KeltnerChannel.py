from .Agent import Agent
import ta.volatility as volatility
import pandas as pd


class KeltnerChannelAgent(Agent):
    def __init__(self, window=20, window_atr=10):
        self.window = window
        self.window_atr = window_atr
        self.column_name = f"keltner_{window}_{window_atr}"
        self.n_outputs = 3

    def prepare_data(self, data: pd.DataFrame) -> pd.Series:
        keltner = volatility.KeltnerChannel(data["High"], data["Low"], data["Close"], self.window, self.window_atr)
        return keltner.keltner_channel_pband()

    def get_signal(self, prepared_data) -> int:
        if prepared_data[self.column_name].iloc[-1] < 0.2:
            return 2
        elif prepared_data[self.column_name].iloc[-1] > 0.8:
            return 1
        else:
            return 0

    def id(self) -> str:
        return self.column_name
