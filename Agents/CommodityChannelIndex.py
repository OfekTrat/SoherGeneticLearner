from .Agent import Agent
import ta.trend as trend


class CCIAgent(Agent):
    def __init__(self, window=20):
        super().__init__()
        self.window = window
        self.column_name = f"cci_{window}"
        self.n_outputs = 3

    def prepare_data(self, data):
        cci = trend.CCIIndicator(data["High"], data["Low"], data["Close"], self.window)
        data[self.column_name] = cci.cci()

    def get_signal(self, prepared_data):
        if prepared_data[self.column_name].iloc[-1] > 100:
            return 2  # OVERBOUGHT
        elif prepared_data[self.column_name].iloc[-1] < -100:
            return 1  # OVERSOLD
        else:
            return 0

    def id(self):
        return self.column_name
