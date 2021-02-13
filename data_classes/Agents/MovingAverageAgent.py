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

    @staticmethod
    def get_signal(prepared_data: pd.DataFrame) -> int:
        if prepared_data.iloc[-2]["sma_small"] < prepared_data.iloc[-2]["sma_big"] and \
                prepared_data.iloc[-1]["sma_small"] > prepared_data.iloc[-1]["sma_big"]:
            return 1
        elif prepared_data.iloc[-2]["sma_small"] > prepared_data.iloc[-2]["sma_big"] and \
                prepared_data.iloc[-1]["sma_small"] < prepared_data.iloc[-1]["sma_big"]:
            return 2
        else:
            return 0

    def prepare_data(self, data):
        data["sma_small"] = data["Close"].rolling(self.small_window).mean()
        data["sma_big"] = data["Close"].rolling(self.big_window).mean()

    def id(self):
        return "sma_id_" + str(self.small_window) + "-" + str(self.big_window)
