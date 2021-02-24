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
        self.n_outputs = 4

    @staticmethod
    def get_signal(prepared_data):
        if 0 < prepared_data["adx"].iloc[-1] < 25:
            return 0
        elif 25 < prepared_data["adx"].iloc[-1] < 50:
            return 1
        elif 50 < prepared_data["adx"].iloc[-1] < 75:
            return 2
        else:
            return 3

    def prepare_data(self, data):
        adx_ind = trend.ADXIndicator(data["High"], data["Low"], data["Close"])
        data["adx"] = adx_ind.adx()

    def id(self):
        return "adx_id"
