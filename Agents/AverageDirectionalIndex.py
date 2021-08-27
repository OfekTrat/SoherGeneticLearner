import ta.trend as trend
from .Agent import Agent

import warnings
warnings.filterwarnings("ignore")


AGENT_TYPE = "ADX"


class ADXAgent(Agent):
    def __init__(self):
        super().__init__()
        self.n_outputs = 4
        self.column_name = "adx"

    def get_signal(self, prepared_data):
        if 0 < prepared_data[self.column_name].iloc[-1] <= 25:
            return 0
        elif 25 < prepared_data[self.column_name].iloc[-1] <= 50:
            return 1
        elif 50 < prepared_data[self.column_name].iloc[-1] <= 75:
            return 2
        else:
            return 3

    def prepare_data(self, data):
        adx_ind = trend.ADXIndicator(data["High"], data["Low"], data["Close"])
        data[self.column_name] = adx_ind.adx()



    def id(self):
        return self.column_name