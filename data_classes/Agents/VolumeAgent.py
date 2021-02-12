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

    def get_signal(self, data: pd.DataFrame) -> int:
        data_copy = data.copy()
        data_copy["sma_small"] = data_copy["Volume"].rolling(self.small_window).mean()
        data_copy["sma_large"] = data_copy["Volume"].rolling(self.large_window).mean()

        if data_copy.iloc[-1]["sma_small"] > data_copy.iloc[-1]["sma_large"]:
            return 1
        else:
            return 0

    def id(self):
        return "volume_id_" + str(self.small_window) + "-" + str(self.large_window)

