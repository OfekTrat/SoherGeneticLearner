from .Agent import Agent
import ta.trend as trend


class TRIXAgent(Agent):
    def __init__(self, window=15):
        super().__init__()
        self.window = window

        self.column_name = f"trix_{window}"
        self.n_outputs = 2

    def prepare_data(self, data):
        trix = trend.TRIXIndicator(data["Close"], self.window)
        data[self.column_name] = trix.trix()

    def get_signal(self, prepared_data):
        if prepared_data[self.column_name].iloc[-1] > 0:
            return 1  # BULL
        else:
            return 0  # BEAR

    def id(self):
        return self.column_name