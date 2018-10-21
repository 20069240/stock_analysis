# -*- coding: utf-8 -*-
# stock_analysis.py

import os, sys # operating system interface
# import from_db as fdb # MySQL instance
import datetime as dt, time # date & time
from pandas.tseries import holiday, offsets # U.S. business (trading) days
import tech_analysis as tech # technical indicators
import pandas as pd, numpy as np # data analysis & wrangling
from tradingWithPython.lib import yahooFinance as yf # historical financial data

"""Add symbols manually or S&P500 symbols from MySQL instance"""
symbols = ['WFC','ORCL','JNJ','MSFT','VZ','DIS','WMT','MCD','TGT','COKE'] # add tickers
# symbols = fdb.symbols[8:16] # pull symbols directly from database

print("Python: {}\n".format(sys.version)) # python version & enviroment

start = 2000/1/1 # set starting date for historic data
tz = os.environ['TZ']='America/New_York' # set local timezone
today = dt.date.today() # current day
now = dt.datetime.now() # current time

stock_count = len(symbols) # ticker list size
stock_size = int(stock_count/2)

# create series of all business (trading) days
us_bd = offsets.CustomBusinessDay(calendar=holiday.USFederalHolidayCalendar())
bdays = pd.Series(pd.date_range(start, today, freq=us_bd, name='Date'))

print (tz + '\n' + now.strftime('%I:%M:%S%p') + ' ' + today.strftime('%m/%d/%Y') + '\n\n' + 
       'Downloading Data for %s Stocks...\n' % stock_count)

try:
    stocks = {s: yf.getHistoricData(s, start) for s in symbols}
    stocks = {s: tech.analyze(stocks[s]) for s in symbols}
except Exception as e:
    pass

elapsed = dt.datetime.now() - now
print(('\n' 'Completed Successfully in %s') % elapsed)

for s in symbols:
    stocks[s]["Date"] = stocks[s].index.date
    stocks[s].set_index("Date", drop=True, inplace=True)
    
close = pd.DataFrame({s: stocks[s]['adj_close'] for s in symbols})
closefill = close.fillna(1)

# normalize adjusted close price for all stocks (scale: 1-100)
high_cl = close.max()
highest_cl = high_cl.max()
normalized = (close/highest_cl) * 100

# get the first & last traded price for each stock
first_close = close.head(1).transpose()
last_close = close.tail(1).transpose()

# calculate up days, cummulative return & daily price change for each stock
daily_return = closefill.apply(lambda x: x / x[0])
stock_change = close.apply(lambda x: np.log(x) - np.log(x.shift(1)))
stock_change = stock_change.fillna(0)
dataDiff = close.diff()[1:]
countPositive = dataDiff > 0
upDays = pd.DataFrame(countPositive.sum())
total_return = daily_return.tail(1).transpose()
        
# start plotting data
daily_return.plot(grid = True, title = 'Cummulative Return (Percent)', lw = .5
                  ).axhline(y = 1, color = "black", lw = 2)
stock_change.plot(grid = True, title = 'Price Change (Percent)', lw = .5
                  ).axhline(y = 0, color = "black", lw = 2)
close.plot(grid = True, subplots=True, title = 'Adjusted Close (Seperated)', 
           lw = .5, layout=(stock_size, 2))
close.plot(grid = True, title = 'Adjusted Close (Price)', lw = .5)
normalized.plot(grid = True, title = 'Adjusted Close (Normalized)', lw = .5)
