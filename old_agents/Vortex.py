from agent_interfaces.Agent import IAgent
import ta.trend as trend
import pandas as pd


class VortexIAgent(IAgent):
    def __init__(self, window=14):
        self.window = window
        self.column_name = f"vortex_{window}"
        self.n_outputs = 2

    def prepare_data(self, data: pd.DataFrame) -> pd.Series:
        vortex = trend.VortexIndicator(data["High"], data["Low"], data["Close"], self.window)
        return vortex.vortex_indicator_diff()

    def get_signal(self, prepared_data: pd.DataFrame) -> int:
        if prepared_data[self.column_name].iloc[-1] > 0:
            return 1  # BULL
        else:
            return 0  # BEAR

    def id(self) -> str:
        return self.column_name
