from agent_interfaces.Agent import IAgent
import ta.momentum as momentum
import pandas as pd



class TSIIAgent(IAgent):
    def __init__(self, slow_window=25, fast_window=13):
        self.slow_window = slow_window
        self.fast_window = fast_window

        self.column_name = f"tsi_{slow_window}_{fast_window}"
        self.n_outputs = 2

    def prepare_data(self, data: pd.DataFrame) -> pd.Series:
        tsi = momentum.TSIIndicator(data["Close"], self.slow_window, self.fast_window)
        return tsi.tsi()

    def get_signal(self, prepared_data: pd.DataFrame) -> int:
        if prepared_data[self.column_name].iloc[-1] > 0:
            return 1  # BUY
        else:
            return 0  # SELL

    def id(self) -> str:
        return self.column_name
