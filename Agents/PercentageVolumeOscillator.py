from .Agent import Agent
import pandas as pd
import ta.momentum as momentum


class PVOAgent(Agent):
    def __init__(self, slow_window=26, fast_window=12, signal_window=9):
        super().__init__()
        self.slow_window = slow_window
        self.fast_window = fast_window
        self.signal_window = signal_window

        self.column_name = f"pvo_{slow_window}_{fast_window}_{signal_window}"
        self.n_outputs = 2

    def prepare_data(self, data):
        pvo = momentum.PercentageVolumeOscillator(data["Volume"], self.slow_window, self.fast_window, self.signal_window)
        data[self.column_name] = pvo.pvo_signal()

    def get_signal(self, prepared_data):
        if prepared_data[self.column_name].iloc[-1] > 0:
            return 1
        else:
            return 0

    def id(self):
        return self.column_name
