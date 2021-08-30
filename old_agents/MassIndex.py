from agent_interfaces.Agent import IAgent
import ta.trend as trend
import pandas as pd


class MIIAgent(IAgent):
    def __init__(self, fast_window=9, slow_window=25):
        self.fast_window = fast_window
        self.slow_window = slow_window

        self.column_name = f'mi_{fast_window}_{slow_window}'
        self.n_outputs = 2

    def prepare_data(self, data: pd.DataFrame) -> pd.Series:
        mi = trend.MassIndex(data["High"], data["Low"], self.fast_window, self.slow_window)
        return mi.mass_index()

    def get_signal(self, prepared_data: pd.DataFrame) -> int:
        if prepared_data[self.column_name].iloc[-1] > 26.5:
            return 1  # TREND REVERSAL
        else:
            return 0  # NO REVERSAL

    def id(self) -> str:
        return self.column_name
