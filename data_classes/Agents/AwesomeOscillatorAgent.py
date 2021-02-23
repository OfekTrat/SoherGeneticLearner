from .Agent import Agent
import pandas as pd
import ta.momentum as momentum

## The signals can be implemented differently


class AwesomeOscillatorAgent(Agent):
    def __init__(self, small_window=5, large_window=34):
        self.small_window = small_window
        self.large_window = large_window
        self.column_name = f"awesome_oscillator_{small_window}_{large_window}"
        self.n_outputs = 3

        super().__init__(self.id())

    def prepare_data(self, data: pd.DataFrame):
        ao = momentum.AwesomeOscillatorIndicator(data["High"], data["Low"], self.small_window, self.large_window)
        data[self.column_name] = ao.awesome_oscillator()

    def get_signal(self, prepared_data: pd.DataFrame):
        if prepared_data[self.column_name].iloc[-1] > 0 > prepared_data[self.column_name].iloc[-2]:
            return 1  # BUY
        elif prepared_data[self.column_name].iloc[-1] < 0 < prepared_data[self.column_name].iloc[-2]:
            return 2  # SELL
        else:
            return 0

    def id(self):
        return self.column_name
