import pandas as pd
from agent_interfaces.Agent import IAgent
from utils.trend_detector import detect_trends


class TrendIAgent(IAgent):
    def __init__(self):
        self.n_outputs = 3

    @staticmethod
    def get_signal(prepared_data: pd.DataFrame) -> int:
        if not prepared_data["UpTrend"].iloc[-1] and not prepared_data["DownTrend"].iloc[-1]:
            return 0
        elif prepared_data["UpTrend"].iloc[-1] and not prepared_data["DownTrend"].iloc[-1]:
            return 1
        else:
            return 2

    def prepare_data(self, data: pd.DataFrame) -> pd.DataFrame:
        return detect_trends(data)

    def id(self) -> str:
        return "trend_id"
