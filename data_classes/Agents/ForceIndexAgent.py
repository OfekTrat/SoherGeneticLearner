from .Agent import Agent
import ta.volume as volume


class ForceIndexAgent(Agent):
    def __init__(self, window=13):
        self.window = window
        self.column_name = f"force_{window}"

    def prepare_data(self, data):
        force = volume.ForceIndexIndicator(data["Close"], data["Volume"], self.window)
        data[self.column_name] = force.force_index()

    def get_signal(self, prepared_data):
        if prepared_data[self.column_name].iloc[-1] > 0:
            return 1  # BUY
        else:
            return 0  # SELL

    def id(self):
        return self.column_name
