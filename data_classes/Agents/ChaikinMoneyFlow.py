from .Agent import Agent
import ta.volume as volume


class CHFAgent(Agent):
    def __init__(self, window=20):
        super().__init__()
        self.window = window
        self.column_name = f"chaikin_{window}"
        self.n_outputs = 2

    def prepare_data(self, data):
        chf = volume.ChaikinMoneyFlowIndicator(data["High"], data["Low"], data["Close"], data["Volume"], self.window)
        data[self.column_name] = chf.chaikin_money_flow()

    def get_signal(self, prepared_data):
        if prepared_data[self.column_name].iloc[-1] > 0:
            return 1  # BUY
        else:
            return 0  # SELL

    def id(self):
        return self.column_name
