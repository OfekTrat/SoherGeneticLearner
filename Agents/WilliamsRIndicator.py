from agent_interfaces.abs_agent import AbsAgent
from agent_interfaces.isignaler import ISignaler
import ta.momentum as momentum
import pandas as pd


class WilliamRIAgent(AbsAgent, ISignaler):
    def __init__(self, lbp=14):
        super().__init__()
        self.lbp = 14
        self.column_name = f"william_r_{lbp}"
        self.n_outputs = 3

    def prepare_data(self, data: pd.DataFrame) -> pd.Series:
        william = momentum.WilliamsRIndicator(data["High"], data["Low"], data["Close"], self.lbp)
        return self._change_column_name(william.williams_r())

    def get_signal(self, prepared_data: pd.DataFrame) -> int:
        if -20 < prepared_data[self.column_name].iloc[-1] < 0:
            return 2  # OVERBOUGHT
        elif -100 < prepared_data[self.column_name].iloc[-1] < -80:
            return 1  # OVERSOLD
        else:
            return 0

    def id(self) -> str:
        return self.column_name
