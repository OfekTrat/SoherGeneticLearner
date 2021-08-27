from .Agent import Agent
import ta.trend as trend


class ICAgent(Agent):
    def __init__(self, window1=9, window2=26, window3=52):
        super().__init__()
        self.window1 = window1
        self.window2 = window2
        self.window3 = window3

        self.column_name = f"ichimoku_{window1}_{window2}_{window3}"
        self.n_outputs = 2

    def prepare_data(self, data):
        ichimoku = trend.IchimokuIndicator(data["High"], data["Low"], self.window1, self.window2, self.window3)
        data[self.column_name] = ichimoku.ichimoku_conversion_line() - ichimoku.ichimoku_base_line()

    def get_signal(self, prepared_data):
        if prepared_data[self.column_name].iloc[-1] > 0:
            return 1  # BULL
        else:
            return 0  # BEAR

    def id(self):
        return self.column_name
