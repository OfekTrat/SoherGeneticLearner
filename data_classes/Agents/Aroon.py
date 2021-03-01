from .Agent import Agent
import ta.trend as trend


class AroonAgent(Agent):
    def __init__(self, window=25):
        super().__init__()
        self.window = window
        self.column_name = f'aroon_{window}'
        self.n_outputs = 2

    def prepare_data(self, data):
        aroon = trend.AroonIndicator(data["Close"], self.window)
        data[self.column_name] = aroon.aroon_indicator()

    def get_signal(self, prepared_data):
        if prepared_data[self.column_name].iloc[-1] > 0:
            return 1  # BULL
        else:
            return 0  # BEAR

    def id(self):
        return self.column_name
