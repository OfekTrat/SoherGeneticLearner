from .Agent import Agent
import ta.trend as trend


class VortexAgent(Agent):
    def __init__(self, window=14):
        super().__init__()
        self.window = window

        self.column_name = f"vortex_{window}"
        self.n_outputs = 2

    def prepare_data(self, data):
        vortex = trend.VortexIndicator(data["High"], data["Low"], data["Close"], self.window)
        data[self.column_name] = vortex.vortex_indicator_diff()

    def get_signal(self, prepared_data):
        if prepared_data[self.column_name].iloc[-1] > 0:
            return 1  # BULL
        else:
            return 0  # BEAR

    def id(self):
        return self.column_name
