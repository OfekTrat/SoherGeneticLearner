from .Agent import Agent
import pandas as pd
import ta.momentum as momentum


class StochasticRSIAgent(Agent):
    def __init__(self, window=14, smooth1=3, smooth2=3):
        self.window = window
        self.smooth1 = smooth1
        self.smooth2 = smooth2

        self.column_name = f"stoch_rsi_{window}_{smooth1}_{smooth2}"

    def prepare_data(self, data):
        stoch_rsi = momentum.StochRSIIndicator(data["Close"], self.window, self.smooth1, self.smooth2)
        data[self.column_name] = stoch_rsi.stochrsi()

    def get_signal(self, prepared_data):
        if prepared_data[self.column_name].iloc[-1] > 0.80:
            return 2  # SELL OVERBOUGHT
        elif prepared_data[self.column_name].iloc[-1] < 0.20:
            return 1  # BUY OVERSOLD
        else:
            return 0

    def id(self):
        return self.column_name