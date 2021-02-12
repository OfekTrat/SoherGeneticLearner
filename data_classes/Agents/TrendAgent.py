import pandas as pd
from .Agent import Agent
from utils.trend_detector import detect_trends


AGENT_TYPE = "Trend"


class TrendAgent(Agent):
    TYPE = AGENT_TYPE

    def __init__(self):
        super().__init__(AGENT_TYPE)
        self.mapper = {
            0: "NOTREND",
            1: "UPTREND",
            2: "DOWNTREND"
        }
        self.n_outputs = 3

    def get_signal(self, data: pd.DataFrame) -> int:
        trends = detect_trends(data)

        if not trends["UpTrend"].iloc[-1] and not trends["DownTrend"].iloc[-1]:
            return 0
        elif trends["UpTrend"].iloc[-1] and not trends["DownTrend"].iloc[-1]:
            return 1
        else:
            return 2

    def id(self):
        return "trend_id"
