import pandas as pd
from abc import ABC


class AbsAgent():
    def _change_column_name(self, data: pd.Series) -> pd.Series:
        data.name = self.column_name
        return data
