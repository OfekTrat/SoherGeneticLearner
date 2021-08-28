from .Agent import Agent
import ta.trend as trend
import pandas as pd


class STCAgent(Agent):
    def __init__(self, slow_window=50, fast_window=23, cycle=10, smooth1=3, smooth2=3):
        self.slow_window = slow_window
        self.fast_window = fast_window
        self.cycle = cycle
        self.smooth1 = smooth1
        self.smooth2 = smooth2
        self.column_name = f"stc_{slow_window}_{fast_window}_{cycle}_{smooth1}_{smooth2}"
        self.n_outputs = 3

    def prepare_data(self, data: pd.DataFrame) -> pd.Series:
        stc = trend.STCIndicator(data["Close"], self.slow_window, self.fast_window,
                                 self.cycle, self.smooth1, self.smooth2)

        return stc.stc()

    def get_signal(self, prepared_data: pd.DataFrame) -> int:
        if 25 < prepared_data[self.column_name].iloc[-1] < 75:
            return 1
        elif prepared_data[self.column_name].iloc[-1] > 75:
            return 2
        else:
            return 0

    def id(self) -> str:
        return self.column_name
