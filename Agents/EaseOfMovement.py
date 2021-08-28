from .Agent import Agent
import ta.volume as volume
import pandas as pd


class EMVAgent(Agent):
    def __init__(self, window=14):
        self.window = window
        self.column_name = f"emv_{window}"
        self.n_outputs = 2

    def prepare_data(self, data: pd.DataFrame) -> pd.Series:
        emv = volume.EaseOfMovementIndicator(data["High"], data["Low"], data["Volume"], self.window)
        return emv.sma_ease_of_movement()

    def get_signal(self, prepared_data: pd.DataFrame) -> int:
        if prepared_data[self.column_name].iloc[-1] > 0:
            return 1  # BUY
        else:
            return 0  # SELL

    def id(self) -> str:
        return self.column_name
