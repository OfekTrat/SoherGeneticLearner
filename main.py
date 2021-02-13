import copy
import pandas as pd
import yfinance as yf
from IPython.display import display
from TreeEnvironment.TreeEnv import TreeEnv


def main():
    tick = yf.Ticker("BLNK")
    data = tick.history("1Y")

    score, generation = TreeEnv.train(data)
    display(score)


if __name__ == '__main__':
    main()
