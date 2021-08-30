import pandas as pd
from agent_interfaces.isignaler import ISignaler
from .ifitness import IFitness


class SimpleFitness(IFitness):
    WINDOW = 2

    @classmethod
    def run(cls, agent: ISignaler, data: pd.DataFrame) -> float:
        signals = cls.__calc_signals(agent, data)
        signals = pd.DataFrame({"price": data.Close, "signal": signals})
        profits = cls.__calc_profits(signals)
        return profits

    @classmethod
    def __calc_signals(cls, agent: ISignaler, data: pd.DataFrame) -> pd.Series:
        return data.rolling(window=cls.WINDOW).apply(
            lambda window: cls.__print_window(data, agent, window)
        ).iloc[:, 0]

    @classmethod
    def __print_window(cls, data: pd.DataFrame, agent: ISignaler, window: pd.Series) -> int:
        data_slice = data.loc[window.index]
        return agent.get_signal(data_slice)

    @classmethod
    def __calc_profits(cls, signals: pd.DataFrame) -> float:
        no_hold_signals = signals[signals.signal != 0]
        profits = no_hold_signals.rolling(window=2).apply(lambda window: cls.__get_profit(window, signals))
        profits = profits.fillna(0)
        return sum(profits.price)

    @classmethod
    def __get_profit(cls, window: pd.Series, signals: pd.DataFrame) -> float:
        data_slice = signals.loc[window.index].fillna(0)

        if data_slice.iloc[0].signal == 1 and data_slice.iloc[1].signal == 2:
            return data_slice.iloc[1].price - data_slice.iloc[0].price
        else:
            return 0
