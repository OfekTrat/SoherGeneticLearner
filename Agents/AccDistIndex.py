import pandas as pd
from agent_interfaces.abs_agent import AbsAgent
from agent_interfaces.isignaler import ISignaler
import ta.volume as volume


class ADIIAgent(AbsAgent, ISignaler):
    def __init__(self):
        super().__init__()
        self.column_name = "adi"
        self.n_outputs = 3

    def prepare_data(self, data: pd.DataFrame) -> pd.Series:
        adi = volume.AccDistIndexIndicator(data["High"], data["Low"], data["Close"], data["Volume"])
        return self._change_column_name(adi.acc_dist_index())

    def get_signal(self, prepared_data):
        if prepared_data[self.column_name].iloc[-1] > 0.5:
            return 1
        elif prepared_data[self.column_name].iloc[-1] < -0.5:
            return 2
        else:
            return 0

    def id(self):
        return self.column_name
