from Agents.StochasticAgent import StochasticAgent
import yfinance as yf
import pandas as pd


tick = yf.Ticker("AMZN")
data = tick.history("1Y")
a = StochasticAgent()

flag = False
amount = 0

for i in range(3, len(data)):
    tmp_data = data.iloc[:i]
    sig = a.get_signal(tmp_data)
    
    if sig == 1 and flag == False:
        amount -= tmp_data.iloc[-1]["Close"] * 10
        flag = True
    elif sig == 2 and flag == True:
        amount += tmp_data.iloc[-1]["Close"] * 10
        flag = False

if flag == True:
    amount += data.iloc[-1]["Close"]
        
print(amount)