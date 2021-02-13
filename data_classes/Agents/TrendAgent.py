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

    @staticmethod
    def get_signal(prepared_data: pd.DataFrame) -> int:
        if not prepared_data["UpTrend"].iloc[-1] and not prepared_data["DownTrend"].iloc[-1]:
            return 0
        elif prepared_data["UpTrend"].iloc[-1] and not prepared_data["DownTrend"].iloc[-1]:
            return 1
        else:
            return 2

    def prepare_data(self, data):
        detect_trends(data)

    def id(self):
        return "trend_id"
