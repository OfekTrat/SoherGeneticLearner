from agent_interfaces.abs_agent import AbsAgent
from agent_interfaces.isignaler import ISignaler
import ta.momentum as momentum
import pandas as pd


class UltimateOscillatorIAgent(AbsAgent, ISignaler):
    def __init__(self, window1=7, window2=14, window3=28):
        super().__init__()
        self.window1 = window1
        self.window2 = window2
        self.window3 = window3

        self.column_name = f"ultimate_{window1}_{window2}_{window3}"
        self.n_outputs = 3

    def prepare_data(self, data: pd.DataFrame) -> pd.Series:
        uo = momentum.UltimateOscillator(data["High"], data["Low"], data["Close"], self.window1, self.window2,
                                         self.window3)
        return self._change_column_name(uo.ultimate_oscillator())

    def get_signal(self, prepared_data: pd.DataFrame) -> int:
        if prepared_data[self.column_name].iloc[-1] < 30:
            return 1  # OVERSOLD
        elif prepared_data[self.column_name].iloc[-1] > 70:
            return 2  # OVERBOUGHT
        else:
            return 0

    def id(self) -> str:
        return self.column_name
