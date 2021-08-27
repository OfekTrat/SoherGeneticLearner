from .Agent import Agent
import ta.volatility as volatility


class UlcerIndexAgent(Agent):
    def __init__(self, window=14):
        super().__init__()
        self.window = window
        self.column_name = f"ulcer_{window}"
        self.n_outputs = 2

    def prepare_data(self, data):
        ulcer = volatility.UlcerIndex(data["Close"], self.window)
        data[self.column_name] = ulcer.ulcer_index()

    def get_signal(self, prepared_data):
        if prepared_data[self.column_name].iloc[-1] > 8:
            return 1  #  SHOULD SELL
        else:
            return 0

    def id(self):
        return self.column_name
