from .Agent import Agent
import ta.trend as trend


class DPOAgent(Agent):
    def __init__(self, window=20):
        super().__init__()
        self.window = window
        self.column_name = f"dpo_{window}"
        self.n_outputs = 2

    def prepare_data(self, data):
        dpo = trend.DPOIndicator(data["Close"], self.window)
        data[self.column_name] = dpo.dpo()

    def get_signal(self, prepared_data):
        if prepared_data[self.column_name].iloc[-1] > 0:
            return 1  # PRICE ABOVE AVG
        else:
            return 0  # PRICE BELOW AVG

    def id(self):
        return self.column_name
