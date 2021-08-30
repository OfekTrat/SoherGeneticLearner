import pandas as pd
import ta.trend as trend
from agent_interfaces.abs_agent import AbsAgent
from agent_interfaces.isignaler import ISignaler

import warnings
warnings.filterwarnings("ignore")


class ADXIAgent(AbsAgent, ISignaler):
    def __init__(self):
        super().__init__()
        self.n_outputs = 4
        self.column_name = "adx"

    def get_signal(self, prepared_data: pd.DataFrame) -> int:
        if 0 < prepared_data[self.column_name].iloc[-1] <= 25:
            return 0
        elif 25 < prepared_data[self.column_name].iloc[-1] <= 50:
            return 1
        elif 50 < prepared_data[self.column_name].iloc[-1] <= 75:
            return 2
        else:
            return 3

    def prepare_data(self, data: pd.DataFrame) -> pd.Series:
        adx_ind = trend.ADXIndicator(data["High"], data["Low"], data["Close"])
        return self._change_column_name(adx_ind.adx())

    def id(self) -> str:
        return self.column_name
