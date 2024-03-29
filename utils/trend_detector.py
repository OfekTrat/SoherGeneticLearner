import pandas as pd
import numpy as np
from statsmodels.tsa.filters.hp_filter import hpfilter


DEV_RANGE = 0.1
HP_FILTER_CONST = 400


def detect_trends(data: pd.DataFrame, window_size=5, column_name="Close") -> pd.DataFrame:
    data.reset_index(inplace=True)

    cycle, trend = hpfilter(data[column_name])
    try:
        function = calc_function(trend)
    except Exception as e:
        raise e

    derivatives = get_derivatives(function)
    return get_trends(data, derivatives, trend.index, window_size)


def calc_function(trend):
    fit_polynomial = np.polyfit(trend.index, trend, deg=50)
    function = np.poly1d(fit_polynomial)
    return function


def get_derivatives(function):
    return np.polyder(function)


def get_trends(data: pd.DataFrame, deriviatives: np.poly1d, indices, window_size) -> pd.DataFrame:
    data_copy = data.copy()
    devs = deriviatives(indices)
    data_copy["UpTrend"] = 0
    data_copy["DownTrend"] = 0

    count_up_trend = 0
    count_down_trend = 0
    trend_exists = 1

    for i in range(0, len(devs) - window_size):
        tmp_devs = devs[i:i + window_size]

        for tmp in tmp_devs:
            if tmp > DEV_RANGE:
                count_up_trend += 1
            elif tmp < -1 * DEV_RANGE:
                count_down_trend += 1

        if count_down_trend == window_size:
            data_copy.loc[i + window_size, "DownTrend"] = trend_exists
        elif count_up_trend == window_size:
            data_copy.loc[i + window_size, "UpTrend"] = trend_exists

        count_up_trend = 0
        count_down_trend = 0

    return data_copy[["UpTrend", "DownTrend"]]
