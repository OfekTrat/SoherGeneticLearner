from agent_interfaces.abs_agent import AbsAgent
from agent_interfaces.isignaler import ISignaler
import pandas as pd
import ta.momentum as momentum


class ROCIAgent(AbsAgent, ISignaler):
    TREND_RANGE = 2

    def __init__(self, window=12):
        super().__init__()
        self.window = window
        self.column_name = f"roc_{window}"
        self.n_outputs = 3

    def prepare_data(self, data: pd.DataFrame) -> pd.Series:
        roc = momentum.ROCIndicator(data["Close"], self.window)
        return self._change_column_name(roc.roc())

    def get_signal(self, prepared_data: pd.DataFrame) -> int:
        if prepared_data[self.column_name].iloc[-1] > self.TREND_RANGE:
            return 1  # TREND UP
        elif prepared_data[self.column_name].iloc[-1] < -1 * self.TREND_RANGE:
            return 2  # TREND DOWN
        else:
            return 0

    def id(self) -> str:
        return self.column_name
