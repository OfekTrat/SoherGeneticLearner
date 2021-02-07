import pandas as pd
from datetime import datetime


LARGE_INTERVAL = 20
SMALL_INTERVAL = 5

TIME_INTERVAL_FOR_HP = 30

START = datetime(2016, 1, 1)
END = datetime.now()


class Agent(object):
    def __init__(self, type: str):
        self.type = type
    
    def print_type(self):
        print(self.type)
