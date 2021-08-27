import os
import pandas as pd
import yfinance as yf
from datetime import datetime
from typing import Optional, List, Dict, Union


class StockDataCollector:
    @classmethod
    def collect(cls, stock_symbols: Union[List[str], str], interval: str = "1d",
                from_time: Optional[datetime] = None, to_time: Optional[datetime] = None) -> Dict[str, pd.DataFrame]:
        stocks = cls.__get_stocks_list(stock_symbols)

        stocks_data = {stock_name: cls.__fetch_data(stock_name, interval, from_time, to_time)
                       for stock_name in stocks}
        return stocks_data

    @classmethod
    def __get_stocks_list(cls, stock_symbols: Union[List[str], str]) -> List[str]:
        if isinstance(stock_symbols, str):
            return [stock_symbols]

        return stock_symbols

    @classmethod
    def __fetch_data(cls, stock_symbol: str, interval: str,
                     from_time: Optional[datetime], to_time: Optional[datetime]) -> pd.DataFrame:
        ticker = yf.Ticker(stock_symbol)
        return ticker.history(interval=interval, start=from_time, end=to_time)

    @classmethod
    def save_collection(cls, collected_data: Dict[str, pd.DataFrame], data_folder: str):
        if not os.path.exists(data_folder):
            os.mkdir(data_folder)
        
        for stock_name, stock_data in collected_data.items():
            path = os.path.join(data_folder, stock_name)
            stock_data.to_pickle(path)
