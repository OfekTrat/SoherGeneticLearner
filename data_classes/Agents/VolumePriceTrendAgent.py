from .Agent import Agent
import ta.volume as volume


class VolumePriceTrendAgent(Agent):
    def __init__(self):
        self.column_name = "vpt"

    def prepare_data(self, data):
        vpt = volume.VolumePriceTrendIndicator(data["Close"], data["Volume"])
        data[self.column_name] = vpt.volume_price_trend()

    def get_signal(self, prepared_data):
        if prepared_data[self.column_name].iloc[-1] > 0:
            return 1
        else:
            return 0
