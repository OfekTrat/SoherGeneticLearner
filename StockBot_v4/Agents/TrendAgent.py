import pandas as pd
import numpy as np
from Agents.Agent import Agent
from statsmodels.tsa.filters.hp_filter import hpfilter

import warnings
warnings.filterwarnings("ignore")

DEV_RANGE = 0.1
HP_FILTER_CONST = 400

class TrendAgent(Agent):
    def __init__(self):
        super().__init__("Trend Agent")
        self.signals = {
            0: "NOTREND",
            1: "UPTREND",
            2: "DOWNTREND"
        }
        self.n_outputs = 3
    
    def get_signal(self, data: pd.DataFrame) -> int:
        trends = detect_trends(data)
        
        if trends["UpTrend"].iloc[-1] == None and trends["DownTrend"].iloc[-1] == None:
            return 0
        elif trends["UpTrend"].iloc[-1] != None and trends["DownTrend"].iloc[-1] == None:
            return 1
        else:
            return 2
    

def detect_trends(data: pd.DataFrame, window_size=5, column_name="Close") -> pd.DataFrame:
    data_copy = data.copy()
    data_copy.reset_index(inplace=True)

    cycle, trend = hpfilter(data_copy[column_name], HP_FILTER_CONST)
    function = calc_function(trend)
    deriviatives = get_deriviatives(function)
    get_trends(data_copy, deriviatives, trend.index, window_size)    
    return data_copy
    

def calc_function(trend):
    fit_polynomial = np.polyfit(trend.index, trend, deg=50)
    function = np.poly1d(fit_polynomial)
    return function


def get_deriviatives(function):
    return np.polyder(function)


def get_trends(data: pd.DataFrame, deriviatives: np.poly1d, indices, window_size):
    devs = deriviatives(indices)
    data["UpTrend"] = None
    data["DownTrend"] = None
    
    count_up_trend = 0
    count_down_trend = 0
    trend_exists = 1
    
    for i in range(0, len(devs) - window_size):
        tmp_devs = devs[i:i+window_size]
        
        for tmp in tmp_devs:
            if tmp > DEV_RANGE:
                count_up_trend += 1
            elif tmp < -1 * DEV_RANGE:
                count_down_trend += 1
        
        if count_down_trend == window_size:
            data["DownTrend"].iloc[i+window_size] = trend_exists
            trend_exists += 1
        elif count_up_trend == window_size:
            data["UpTrend"].iloc[i+window_size] = trend_exists
            trend_exists += 1
        else:
            data["DownTrend"].iloc[i+window_size] = None
            data["UpTrend"].iloc[i+window_size] = None
        
        count_up_trend = 0
        count_down_trend = 0
    
