import pandas as pd
from agent_interfaces.isignaler import ISignaler
from typing import Protocol


class IFitness(Protocol):
    @classmethod
    def run(cls, agent: ISignaler, data: pd.DataFrame) -> int:
        raise NotImplementedError
