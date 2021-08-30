from agent_interfaces.Agent import IAgent
import ta.momentum as momentum
import pandas as pd


class WilliamRIAgent(IAgent):
    def __init__(self, lbp=14):
        self.lbp = 14
        self.column_name = f"william_r_{lbp}"
        self.n_outputs = 3

    def prepare_data(self, data: pd.DataFrame) -> pd.Series:
        william = momentum.WilliamsRIndicator(data["High"], data["Low"], data["Close"], self.lbp)
        return william.williams_r()

    def get_signal(self, prepared_data: pd.DataFrame) -> int:
        if -20 < prepared_data[self.column_name].iloc[-1] < 0:
            return 2  # OVERBOUGHT
        elif -100 < prepared_data[self.column_name].iloc[-1] < -80:
            return 1  # OVERSOLD
        else:
            return 0

    def id(self) -> str:
        return self.column_name
