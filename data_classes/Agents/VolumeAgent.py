from .Agent import Agent
import pandas as pd


AGENT_TYPE = "Volume"


class VolumeAgent(Agent):
    def __init__(self, small_window: int, large_window: int):
        self.small_window = small_window
        self.large_window = large_window

        self.column_name = f"volume2_{small_window}_{large_window}"
        self.n_outputs = 2

    @staticmethod
    def get_signal(prepared_data: pd.DataFrame) -> int:
        if prepared_data.iloc[-1]["sma_vol_small"] > prepared_data.iloc[-1]["sma_vol_large"]:
            return 1
        else:
            return 0

    def prepare_data(self, data):
        data[self.column_name] = data["Volume"].rolling(self.small_window).mean() - \
                                 data["Volume"].rolling(self.large_window).mean()

    def id(self):
        return self.column_name

