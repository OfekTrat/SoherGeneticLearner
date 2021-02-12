import pandas as pd
from .Agent import Agent


AGENT_TYPE = "MACA"


class MACAgent(Agent):
    TYPE = AGENT_TYPE

    def __init__(self, small_window: int, big_window: int):
        super().__init__(AGENT_TYPE)
        self.big_window = big_window
        self.small_window = small_window

        self.mapper = {
            1: "BUY",
            2: "SELL",
            0: "NOTHING"
        }
        self.n_outputs = 3

    def get_signal(self, data: pd.DataFrame) -> int:
        data_copy = data.copy()
        data_copy["sma_small"] = data_copy["Close"].rolling(self.small_window).mean()  # SMA - Simple Moving Average
        data_copy["sma_big"] = data_copy["Close"].rolling(self.big_window).mean()

        if data_copy.iloc[-2]["sma_small"] < data_copy.iloc[-2]["sma_big"] and \
                data_copy.iloc[-1]["sma_small"] > data_copy.iloc[-1]["sma_big"]:
            return 1
        elif data_copy.iloc[-2]["sma_small"] > data_copy.iloc[-2]["sma_big"] and \
                data_copy.iloc[-1]["sma_small"] < data_copy.iloc[-1]["sma_big"]:
            return 2
        else:
            return 0

    def id(self):
        return "sma_id_" + str(self.small_window) + "-" + str(self.big_window)
