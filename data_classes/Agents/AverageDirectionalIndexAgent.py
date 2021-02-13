import stockstats
from .Agent import Agent

import warnings
warnings.filterwarnings("ignore")


AGENT_TYPE = "ADX"


class ADXAgent(Agent):
    TYPE = AGENT_TYPE

    def __init__(self):
        super().__init__(AGENT_TYPE)
        self.signals = {
            0: "WeakTrend",
            1: "StrongTrend"
        }
        self.n_outputs = 2

    @staticmethod
    def get_signal(prepared_data):
        if prepared_data["adx"].iloc[-1] > 25:
            return 1
        else:
            return 0

    def prepare_data(self, data):
        data_copy = data.copy()

        data_copy["close"] = data_copy["Close"]
        data_copy["open"] = data_copy["Open"]
        data_copy["high"] = data_copy["High"]
        data_copy["low"] = data_copy["Low"]
        data_copy = data_copy[["low", "close", "high", "open"]]

        data["adx"] = stockstats.StockDataFrame(data_copy)["adx"]

    def id(self):
        return "adx_id"
