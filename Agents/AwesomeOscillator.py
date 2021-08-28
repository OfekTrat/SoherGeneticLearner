from .Agent import Agent
import pandas as pd
import ta.momentum as momentum


class AwesomeOscillatorAgent(Agent):
    def __init__(self, small_window=5, large_window=34):
        self.small_window = small_window
        self.large_window = large_window
        self.column_name = f"awesome_oscillator_{small_window}_{large_window}"
        self.n_outputs = 2

    def prepare_data(self, data: pd.DataFrame) -> pd.Series:
        ao = momentum.AwesomeOscillatorIndicator(data["High"], data["Low"], self.small_window, self.large_window)
        return ao.awesome_oscillator()

    def get_signal(self, prepared_data: pd.DataFrame) -> int:
        if prepared_data[self.column_name].iloc[-1] > 0:
            return 1  # BUY
        else:
            return 0

    def id(self) -> str:
        return self.column_name
