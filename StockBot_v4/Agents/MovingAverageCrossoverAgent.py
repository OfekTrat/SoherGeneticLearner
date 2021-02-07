import pandas as pd
from Agents.Agent import Agent

class MACAgent(Agent):
    def __init__(self, small_interval: int, large_interval: int):
        super().__init__("Moving Average Crossover Agent")
        self.small_interval = small_interval
        self.large_interval = large_interval
        self.signals = {
            0: "NOTHING",
            1: "BUY",
            2: "SELL"
        }
        self.n_outputs = 3
    
    
    def get_signal(self, data: pd.DataFrame) -> int:
        data["SmallMovingAverage"] = data["Close"].rolling(self.small_interval).mean()
        data["LargeMovingAverage"] = data["Close"].rolling(self.large_interval).mean()
        
        if data["SmallMovingAverage"].iloc[-2] < data["LargeMovingAverage"].iloc[-2] and \
            data["SmallMovingAverage"].iloc[-1] > data["LargeMovingAverage"].iloc[-1]:
                return 1
        elif data["SmallMovingAverage"].iloc[-2] > data["LargeMovingAverage"].iloc[-2] and \
            data["SmallMovingAverage"].iloc[-1] < data["LargeMovingAverage"].iloc[-1]:
                return 2
        else:
            return 0
        