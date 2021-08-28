from .Agent import Agent
import ta.volume as volume
import pandas as pd


class MFIAgent(Agent):
    def __init__(self, window=14):
        self.window = window
        self.column_name = f"mfi_{window}"
        self.n_outputs = 3

    def prepare_data(self, data: pd.DataFrame) -> pd.Series:
        mfi = volume.MFIIndicator(data["High"], data["Low"], data["Close"], data["Volume"], self.window)
        return mfi.money_flow_index()

    def get_signal(self, prepared_data: pd.DataFrame) -> int:
        if prepared_data[self.column_name].iloc[-1] > 80:
            return 2  # OVERBOUGHT
        elif prepared_data[self.column_name].iloc[-2] < 20:
            return 1  # OVERSOLD
        else:
            return 0

    def id(self) -> str:
        return self.column_name
