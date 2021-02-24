from .Agent import Agent
import ta.volume as volume


class EMVAgent(Agent):
    def __init__(self, window=14):
        self.window = window
        self.column_name = f"emv_{window}"

    def prepare_data(self, data):
        emv = volume.EaseOfMovementIndicator(data["High"], data["Low"], data["Volume"], self.window)
        data[self.column_name] = emv.sma_ease_of_movement()

    def get_signal(self, prepared_data):
        if prepared_data[self.column_name].iloc[-1] > 0:
            return 1  # BUY
        else:
            return 0  # SELL

    def id(self):
        return self.column_name
