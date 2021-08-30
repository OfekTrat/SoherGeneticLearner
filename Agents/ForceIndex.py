from agent_interfaces.abs_agent import AbsAgent
from agent_interfaces.isignaler import ISignaler
import ta.volume as volume
import pandas as pd


class ForceIndexIAgent(AbsAgent, ISignaler):
    def __init__(self, window=13):
        super().__init__()
        self.window = window
        self.column_name = f"force_{window}"
        self.n_outputs = 2

    def prepare_data(self, data: pd.DataFrame) -> pd.Series:
        force = volume.ForceIndexIndicator(data["Close"], data["Volume"], self.window)
        return self._change_column_name(force.force_index())

    def get_signal(self, prepared_data: pd.DataFrame) -> int:
        if prepared_data[self.column_name].iloc[-1] > 0:
            return 1  # BUY
        else:
            return 0  # SELL

    def id(self) -> str:
        return self.column_name
