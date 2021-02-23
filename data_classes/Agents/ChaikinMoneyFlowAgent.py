from .Agent import Agent
import ta.volume as volume


class CHFAgent(Agent):
    def __init__(self, window=20):
        self.window = window
        self.column_name = f"chaikin_{window}"

    def prepare_data(self, data):
        chf = volume.ChaikinMoneyFlowIndicator(data["High"], data["Low"], data["Close"], data["Volume"], self.window)
        data[self.column_name] = chf.chaikin_money_flow()

    def get_signal(self, prepared_data):
        if prepared_data[self.column_name].iloc[-2] < 0 < prepared_data[self.column_name].iloc[-1]:
            return 1  # BUY
        elif prepared_data[self.column_name].iloc[-2] > 0 > prepared_data[self.column_name].iloc[-1]:
            return 2  # SELL
        else:
            return 0

    def id(self):
        return self.column_name
