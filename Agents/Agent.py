import pandas as pd
from typing import Protocol, Union


class Agent(Protocol):
    def prepare_data(self, data: pd.DataFrame) -> Union[pd.DataFrame, pd.Series]:
        raise NotImplementedError

    def get_signal(self, prepared_data: pd.DataFrame) -> int:
        raise NotImplementedError()

    def id(self) -> str:
        raise NotImplementedError()
