from agent_interfaces.Agent import IAgent
import pandas as pd
import ta.momentum as momentum


class RSIIAgent(IAgent):
    def __init__(self, window=14):
        self.window = window
        self.column_name = f"rsi_{window}"
        self.n_outputs = 3

    def prepare_data(self, data: pd.DataFrame) -> pd.Series:
        rsi = momentum.RSIIndicator(data["Close"], self.window)
        return rsi.rsi()

    def get_signal(self, prepared_data: pd.DataFrame) -> int:
        if prepared_data[self.column_name].iloc[-1] > 70:
            return 2  # SELL
        elif prepared_data[self.column_name].iloc[-1] < 30:
            return 1  # BUY
        else:
            return 0  # NOTHING

    def id(self) -> str:
        return self.column_name