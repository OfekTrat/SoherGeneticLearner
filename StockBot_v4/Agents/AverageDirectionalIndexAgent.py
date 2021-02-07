import stockstats
from Agents.Agent import Agent
import warnings
warnings.filterwarnings("ignore")

class ADXAgent(Agent):
    def __init__(self):
        super().__init__("ADX Agent")
        self.signals = {
            0: "WeakTrend",
            1: "StrongTrend"
        }
        self.n_outputs = 2
        
        
    def get_signal(self, data):
        data["close"] = data["Close"]
        data["open"] = data["Open"]
        data["high"] = data["High"]
        data["low"] = data["Low"]
        data = data[["low", "close", "high", "open"]]
        
        data["adx"] = stockstats.StockDataFrame(data)["adx"]
        
        if data["adx"].iloc[-1] > 25:
            return 1
        else:
            return 0
    
