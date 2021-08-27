from .Agent import Agent
import ta.volume as volume


class ADIAgent(Agent):
    def __init__(self):
        super().__init__()
        self.column_name = "adi"
        self.n_outputs = 3

    def prepare_data(self, data):
        adi = volume.AccDistIndexIndicator(data["High"], data["Low"], data["Close"], data["Volume"])
        data[self.column_name] = adi.acc_dist_index()

    def get_signal(self, prepared_data):
        if prepared_data[self.column_name].iloc[-1] > 0.5:
            return 1
        elif prepared_data[self.column_name].iloc[-1] < -0.5:
            return 2
        else:
            return 0

    def id(self):
        return self.column_name
