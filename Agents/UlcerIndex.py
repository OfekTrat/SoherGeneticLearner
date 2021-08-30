from agent_interfaces.abs_agent import AbsAgent
from agent_interfaces.isignaler import ISignaler
import ta.volatility as volatility
import pandas as pd


class UlcerIndexIAgent(AbsAgent, ISignaler):
    def __init__(self, window=14):
        super().__init__()
        self.window = window
        self.column_name = f"ulcer_{window}"
        self.n_outputs = 2

    def prepare_data(self, data: pd.DataFrame) -> pd.Series:
        ulcer = volatility.UlcerIndex(data["Close"], self.window)
        return self._change_column_name(ulcer.ulcer_index())

    def get_signal(self, prepared_data: pd.DataFrame) -> int:
        if prepared_data[self.column_name].iloc[-1] > 8:
            return 1  #  SHOULD SELL
        else:
            return 0

    def id(self) -> str:
        return self.column_name
