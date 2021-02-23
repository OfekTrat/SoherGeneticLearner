import ta.trend as trend
from .Agent import Agent

import warnings
warnings.filterwarnings("ignore")


AGENT_TYPE = "ADX"


class ADXAgent(Agent):
    TYPE = AGENT_TYPE
    MUTATED_ATTRS = {}

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
        adx_ind = trend.ADXIndicator(data["High"], data["Low"], data["Close"])
        data["adx"] = adx_ind.adx()

    def id(self):
        return "adx_id"
