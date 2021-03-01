from .Agent import Agent
import ta.volatility as volatility


class DonchianChannelAgent(Agent):
    def __init__(self, window=20):
        super().__init__()
        self.window = 20
        self.column_name = f"donchian_{window}"
        self.n_outputs = 3

    def prepare_data(self, data):
        donchian = volatility.DonchianChannel(data["High"], data["Low"], data["Close"], self.window)
        data[self.column_name] = donchian.donchian_channel_pband()

    def get_signal(self, prepared_data):
        if prepared_data[self.column_name].iloc[-1] > 0.8:
            return 1
        elif prepared_data[self.column_name].iloc[-1] < 0.2:
            return 2
        else:
            return 0

    def id(self):
        return self.column_name

