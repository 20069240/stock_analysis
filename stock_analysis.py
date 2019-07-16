# -*- coding: utf-8 -*-

# stock_analysis.py
__author__ = 'adrian'

import os, sys # operating system interface
import datetime as dt, time # date and time
import from_db as fdb # mysql server and database storage
import tech_analysis as tech # technical indicators
from pandas.tseries import holiday, offsets
import pandas as pd, numpy as np # data analysis and wrangling
from tradingWithPython.lib import yahooFinance as yf # historical financial data


# In[0]:
# add symbols manually or s&p500 symbols stored in database
# symbols = ['AAPL','ORCL','AMZN','MSFT','FB','DIS','WMT','MCD'] # manually add symbols
symbols = fdb.symbols[:505] # pull symbols directly from database

print("Python: {}\n".format(sys.version)) #  python version & enviroment

start = 2000/1/1
today = dt.date.today()
now = dt.datetime.now()
tz = os.environ['TZ']='America/New_York' # local time & timezone
t = time.localtime()
time = dt.datetime.now().strftime('%I:%M:%S%p')

stock_count = len(symbols)
stock_size = int(stock_count/2)

# create series of all tradings days within range
us_bd = offsets.CustomBusinessDay(calendar=holiday.USFederalHolidayCalendar())
bdays = pd.Series(pd.date_range(start, today, freq=us_bd, name='Date'))

print (tz + '\n' + time + ' ' + today.strftime('%m/%d/%Y') + '\n\n' +
       'Downloading Data for %s Stocks...\n' % stock_count)

stocks = {}
close_p = {}
first_close = {}
for s in symbols:
    try:
        stocks.update({s: yf.getHistoricData(s, start)})
        stocks.update({s: tech.analyze(stocks[s])})
        stocks[s]["Date"] = stocks[s].index.date
        stocks[s].set_index("Date", drop=True, inplace=True)
        close = pd.DataFrame(close_p.update({s: stocks[s]['adj_close']}))
        first_close.update({s: stocks[s]['adj_close'].head(1).transpose()})
    except:
        pass

#stocks = {s: yf.getHistoricData(s, start) for s in symbols}
#stocks = {s: tech.analyze(stocks[s]) for s in symbols}
#close = pd.DataFrame({s: stocks[s]['adj_close'] for s in symbols})
#first_close = {s: stocks[s]['adj_close'].head(1).transpose() for s in symbols}

closefill = close.fillna(1)
last_close = close.tail(1).transpose()
daily_return = closefill.apply(lambda x: x / x[0])
stock_change = close.apply(lambda x: np.log(x) - np.log(x.shift(1)))
stock_change = stock_change.fillna(0)
dataDiff = close.diff()[1:]
countPositive = dataDiff > 0
upDays = pd.DataFrame(countPositive.sum())
total_return = daily_return.tail(1).transpose()

elapsed = dt.datetime.now() - now
print(('\n' 'Completed Successfully in %s') % elapsed)

# In[1]: start plotting the data
#daily_return.plot(grid = True, title = '% Cummulative Return', lw = 1
                  #).axhline(y = 1, color = "black", lw = 2)
#stock_change.plot(grid = True, title = '% Price Change', lw = 1
                  #).axhline(y = 0, color = "black", lw = 2)
#close.plot(grid = True, lw = 1)
#close.plot(grid = True, subplots=True, lw = 1, layout=(stock_size, 2))

# uncomment to display a candlestick chart for each stock
#import my_modules as mymod
#for s in symbols:
#     mymod.plot_candlestick(stocks[s].loc[dt.date(today.year - 1,
#                            today.month,today.day):today], title=s)
