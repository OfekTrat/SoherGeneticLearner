import pandas as pd
from Agents import Agent
from typing import Protocol


class IFitness(Protocol):
    @classmethod
    def run(cls, agent: Agent, data: pd.DataFrame) -> int:
        raise NotImplementedError
