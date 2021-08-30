from agent_interfaces.Agent import IAgent
import pandas as pd
import ta.momentum as momentum


class PPOIAgent(IAgent):
    def __init__(self, slow_window=26, fast_window=12, signal_window=9):
        self.slow_window = slow_window
        self.fast_window = fast_window
        self.signal_window = signal_window

        self.column_name = f"ppo_{slow_window}_{fast_window}_{signal_window}"
        self.n_outputs = 2

    def prepare_data(self, data: pd.DataFrame) -> pd.Series:
        ppo = momentum.PercentagePriceOscillator(data["Close"], self.slow_window, self.fast_window, self.signal_window)
        return ppo.ppo_signal()

    def get_signal(self, prepared_data) -> int:
        if prepared_data[self.column_name].iloc[-1] > 0:
            return 1  # BUY
        else:
            return 0  # SELL

    def id(self) -> str:
        return self.column_name
