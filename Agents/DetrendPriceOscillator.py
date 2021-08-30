from agent_interfaces.abs_agent import AbsAgent
from agent_interfaces.isignaler import ISignaler
import ta.trend as trend
import pandas as pd


class DPOIAgent(AbsAgent, ISignaler):
    def __init__(self, window=20):
        super().__init__()
        self.window = window
        self.column_name = f"dpo_{window}"
        self.n_outputs = 2

    def prepare_data(self, data: pd.DataFrame) -> pd.Series:
        dpo = trend.DPOIndicator(data["Close"], self.window)
        return self._change_column_name(dpo.dpo())

    def get_signal(self, prepared_data: pd.DataFrame) -> int:
        if prepared_data[self.column_name].iloc[-1] > 0:
            return 1  # PRICE ABOVE AVG
        else:
            return 0  # PRICE BELOW AVG

    def id(self) -> str:
        return self.column_name
