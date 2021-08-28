from .Agent import Agent
import ta.volume as volume
import pandas as pd


class VolumePriceTrendAgent(Agent):
    def __init__(self):
        self.column_name = "vpt"
        self.n_outputs = 2

    def prepare_data(self, data: pd.DataFrame) -> pd.Series:
        vpt = volume.VolumePriceTrendIndicator(data["Close"], data["Volume"])
        return vpt.volume_price_trend()

    def get_signal(self, prepared_data: pd.DataFrame) -> int:
        if prepared_data[self.column_name].iloc[-1] > 0:
            return 1
        else:
            return 0

    def id(self) -> str:
        return self.column_name
