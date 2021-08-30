from agent_interfaces.abs_agent import AbsAgent
from agent_interfaces.isignaler import ISignaler
import ta.trend as trend
import pandas as pd


class PSARIAgent(AbsAgent, ISignaler):
    def __init__(self, step=0.02, max_step=0.2):
        super().__init__()
        self.step = step
        self.max_step = max_step
        self.column_name = f"psar_{step}_{max_step}"
        self.n_outputs = 3

    def prepare_data(self, data: pd.DataFrame) -> pd.Series:
        psar = trend.PSARIndicator(data["High"], data["Low"], data["Close"], self.step, self.max_step)
        pasr_up = psar.psar_up_indicator()
        pasr_up = pasr_up.apply(lambda x: x * 2)
        psar_down = psar.psar_down_indicator()
        psar_indicator = pasr_up + psar_down
        return self._change_column_name(psar_indicator)

    def get_signal(self, prepared_data: pd.DataFrame) -> int:
        return int(prepared_data[self.column_name].iloc[-1].item())

    def id(self) -> str:
        return self.column_name
