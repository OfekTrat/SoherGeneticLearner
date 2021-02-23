from .Agent import Agent
import ta.trend as trend


class KSTAgent(Agent):
    def __init__(self, roc1=10, roc2=15, roc3=20, roc4=30, window1=10, window2=10, window3=10, window4=15):
        self.roc1 = roc1
        self.roc2 = roc2
        self.roc3 = roc3
        self.roc4 = roc4

        self.window1 = window1
        self.window2 = window2
        self.window3 = window3
        self.window4 = window4

        self.column_name = f"kst_{roc1}_{roc2}_{roc3}_{roc4}_{window1}_{window2}_{window3}_{window4}"

    def prepare_data(self, data):
        kst = trend.KSTIndicator(data["Close"], self.roc1, self.roc2, self.roc3, self.roc4,
                                 self.window1, self.window2, self.window3, self.window4)

        data[self.column_name] = kst.kst_diff()

    def get_signal(self, prepared_data):
        if prepared_data[self.column_name] > 0:
            return 1  # BULL
        else:
            return 0  # BEAR

    def id(self):
        return self.column_name