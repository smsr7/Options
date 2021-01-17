import numpy as np
import datetime
from dateutil.relativedelta import relativedelta
from yahoo_fin import stock_info
import pandas as pd
import csv
import matplotlib.pyplot as plt

def get_data(tickers=None, timeframe=4, testing = 6):
    if tickers == None:
         tickers = ["AMD","ADBE","NVDA","BA","CRWD","CGC"]
    for ticker in tickers:
        cur = datetime.datetime.now()
        print(ticker)
        history_data = stock_info.get_data(str(ticker),

        start_date=datetime.datetime(2009,1,1),
        end_date=datetime.datetime(2018,1,1), index_as_date=True, interval="1d")

        history = history_data[["open", "close"]]

        test_data = stock_info.get_data(str(ticker),
        start_date=datetime.datetime(2008,1,1),
        end_date=datetime.datetime(2009,1,1), index_as_date=True, interval="1d")

        test_data = test_data.append(stock_info.get_data(str(ticker),
        start_date=datetime.datetime(2018,1,1),
        end_date=cur, index_as_date=True, interval="1d"))
        test = test_data[["open","close"]]



        hist_data = pd.DataFrame()
        hist_full = pd.DataFrame()

        for i in range(len(history)-1):
            hist_data = hist_data.append(
            {
            'price': history.close.iloc[i] - history.open.iloc[i],
            },
            ignore_index=True)

            hist_full = hist_full.append(
            {
            'price': history.open[i]
            },
            ignore_index=True)
            hist_full = hist_full.append(
            {
            'price': history.close[i]
            },
            ignore_index=True)

            hist_data = hist_data.append(
            {
            'price': history.open.iloc[i+1] - history.close.iloc[i]
            },
            ignore_index=True)


        eval_data = pd.DataFrame()
        test_full = pd.DataFrame()
        for i in range(len(test)-1):
            eval_data = eval_data.append(
            {
            'price': test.close.iloc[i] - test.open.iloc[i],
            },
            ignore_index=True)

            test_full = test_full.append(
            {
            'price': test.open[i]
            },
            ignore_index=True)
            test_full = test_full.append(
            {
            'price': test.close[i]
            },
            ignore_index=True)


            eval_data = eval_data.append(
            {
            'price': test.open.iloc[i+1] - test.close.iloc[i]
            },
            ignore_index=True)

        hist_full.to_csv("data/history/full/"+str(ticker)+"_full.csv",index=False)
        hist_data.to_csv("data/history/"+str(ticker)+".csv",index=False)

        test_full.to_csv("data/testing/full/"+str(ticker)+"_full.csv",index=False)
        eval_data.to_csv("data/testing/"+str(ticker)+".csv",index=False)

if __name__ == '__main__':
    get_data()#tickers=["SPY","QQQ","DIA","WMT","AMZN","XOM","AAPL","CVS","VZ","UNH","MCK","T","ABC","F","CI","COST","CVX","JPM"])
