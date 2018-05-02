# -*- coding: utf-8 -*-

# stock_analysis.py
__author__ = 'adrian aley'

import os, sys # operating system interface
# import from_db as fdb # MySQL server and database storage
import datetime as dt # date and time
from pandas.tseries import holiday, offsets # market calendar
import tech_analysis as tech # technical indicators
import pandas as pd, numpy as np # data analysis and wrangling
from tradingWithPython.lib import yahooFinance as yf # historical financial data

"""add symbols manually or pull s&p500 symbols from MySQL server"""
symbols = ['AAPL','ORCL','AMZN','MSFT','FB','DIS','WMT','MCD'] # manually add symbols
# symbols = fdb.symbols[:8] # pull symbols from MySQL server

print("Python: {}\n".format(sys.version)) #  python version & enviroment

start = 2000/1/1
today = dt.date.today().strftime('%m/%d/%Y')
now = dt.datetime.now()
tz = os.environ['TZ']='America/New_York' # local timezone

stock_count = len(symbols)
stock_size = int(stock_count/2)

# create series of all tradings days within range
us_bd = offsets.CustomBusinessDay(calendar=holiday.USFederalHolidayCalendar())
bdays = pd.Series(pd.date_range(start, today, freq=us_bd, name='Date'))

print (tz + '\n' + now.strftime('%I:%M:%S%p') + ' ' + today + '\n\n' + 
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
first_close = {s: stocks[s]['adj_close'].head(1).transpose() for s in symbols}
last_close = close.tail(1).transpose()
daily_return = close.apply(lambda x: x / x[0])
# cummulative returns
stock_change = close.apply(lambda x: np.log(x) - np.log(x.shift(1)))
stock_change = stock_change.fillna(0)
dataDiff = close.diff()[1:]
countPositive = dataDiff > 0
upDays = pd.DataFrame(countPositive.sum())
total_return = daily_return.tail(1).transpose()
        
# start plotting the data
daily_return.plot(grid = True, title = '% Cummulative Return', lw = 1
                  ).axhline(y = 1, color = "black", lw = 2)
stock_change.plot(grid = True, title = '% Price Change', lw = 1
                  ).axhline(y = 0, color = "black", lw = 2)
close.plot(grid = True, lw = 1)
close.plot(grid = True, subplots=True, lw = 1, layout=(stock_size, 2))
