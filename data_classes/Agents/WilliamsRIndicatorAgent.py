from .Agent import Agent
import ta.momentum as momentum


class WilliamRAgent(Agent):
    def __init__(self, lbp=14):
        self.lbp = 14

        self.column_name = f"william_r_{lbp}"

    def prepare_data(self, data):
        william = momentum.WilliamsRIndicator(data["High"], data["Low"], data["Close"], self.lbp)
        data[self.column_name] = william.williams_r()

    def get_signal(self, prepared_data):
        if -20 < prepared_data[self.column_name].iloc[-1] < 0:
            return 2  # OVERBOUGHT
        elif -100 < prepared_data[self.column_name].iloc[-1] < -80:
            return 1  # OVERSOLD
        else:
            return 0

    def id(self):
        return self.column_name