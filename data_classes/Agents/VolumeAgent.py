from .Agent import Agent
import pandas as pd


AGENT_TYPE = "Volume"


class VolumeAgent(Agent):
    TYPE = AGENT_TYPE

    def __init__(self, small_window: int, large_window: int):
        super().__init__(AGENT_TYPE)
        self.small_window = small_window
        self.large_window = large_window

        self.mapper = {
            1: "STRONG",
            0: "WEAK"
        }
        self.n_outputs = 2

    @staticmethod
    def get_signal(prepared_data: pd.DataFrame) -> int:
        if prepared_data.iloc[-1]["sma_vol_small"] > prepared_data.iloc[-1]["sma_vol_large"]:
            return 1
        else:
            return 0

    def prepare_data(self, data):
        data["sma_vol_small"] = data["Volume"].rolling(self.small_window).mean()
        data["sma_vol_large"] = data["Volume"].rolling(self.large_window).mean()

    def id(self):
        return "volume_id_" + str(self.small_window) + "-" + str(self.large_window)

