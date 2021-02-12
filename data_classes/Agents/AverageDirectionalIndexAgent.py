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

    def get_signal(self, data):
        data["close"] = data["Close"]
        data["open"] = data["Open"]
        data["high"] = data["High"]
        data["low"] = data["Low"]
        data = data[["low", "close", "high", "open"]]

        data["adx"] = stockstats.StockDataFrame(data)["adx"]

        if data["adx"].iloc[-1] > 25:
            return 1
        else:
            return 0

    def id(self):
        return "adx_id"
