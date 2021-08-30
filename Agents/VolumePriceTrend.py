from agent_interfaces.abs_agent import AbsAgent
from agent_interfaces.isignaler import ISignaler
import ta.volume as volume
import pandas as pd


class VolumePriceTrendIAgent(AbsAgent, ISignaler):
    def __init__(self):
        super().__init__()
        self.column_name = "vpt"
        self.n_outputs = 2

    def prepare_data(self, data: pd.DataFrame) -> pd.Series:
        vpt = volume.VolumePriceTrendIndicator(data["Close"], data["Volume"])
        return self._change_column_name(vpt.volume_price_trend())

    def get_signal(self, prepared_data: pd.DataFrame) -> int:
        if prepared_data[self.column_name].iloc[-1] > 0:
            return 1
        else:
            return 0

    def id(self) -> str:
        return self.column_name
