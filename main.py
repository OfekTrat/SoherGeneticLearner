import copy
import pandas as pd
import yfinance as yf
from TreeEnvironment.TreeEnv import TreeEnv

def main():
    tick = yf.Ticker("BLNK")
    data = tick.history("1Y")

    te = TreeEnv()
    te._create_gen()

    score = te.get_trees_score(data)
    print(score)


if __name__ == '__main__':
    main()
