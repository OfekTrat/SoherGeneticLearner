from .Agent import Agent
import pandas as pd
import ta.momentum as momentum


class PPOAgent(Agent):
    def __init__(self, slow_window=26, fast_window=12, signal_window=9):
        self.slow_window = slow_window
        self.fast_window = fast_window
        self.signal_window = signal_window

        self.column_name = f"ppo_{slow_window}_{fast_window}_{signal_window}"

    def prepare_data(self, data):
        ppo = momentum.PercentagePriceOscillator(data["Close"], self.slow_window, self.fast_window, self.signal_window)
        data[self.column_name] = ppo.ppo_signal()

    def get_signal(self, prepared_data):
        if prepared_data[self.column_name].iloc[-2] < 0 < prepared_data[self.column_name].iloc[-1]:
            return 1  # BUY
        elif prepared_data[self.column_name].iloc[-2] > 0 > prepared_data[self.column_name].iloc[-1]:
            return 2  # SELL
        else:
            return 0  # NOTHING

    def id(self):
        return self.column_name
