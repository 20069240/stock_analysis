# -*- coding: utf-8 -*-
# stock_analysis.py

import os, sys # operating system interface
# import from_db as fdb # MySQL instance
import datetime as dt # date & time
import tech_analysis as tech # technical indicators
import pandas as pd, numpy as np # data analysis & wrangling
import matplotlib.pyplot as plt  # plotting data
import seaborn as sns # statistical data visualization
sns.set_style('darkgrid')
from tradingWithPython.lib import yahooFinance as yf # historical financial data

symbols = ['WFC','ORCL','JNJ','MSFT','VZ','DIS','WMT','MCD','TGT','COKE','FB','SNAP']
# symbols = fdb.symbols[8:16] # pull symbols directly from database

start = 2000/1/1 # set starting date for historic data
tz = os.environ['TZ']='America/New_York' # set local timezone
today = dt.date.today() # current day
now = dt.datetime.now() # current time
count = len(symbols) # ticker list size

print ("Python: {}\n\n".format(sys.version) + tz + 
       '\n' + now.strftime('%I:%M:%S%p') + ' ' + today.strftime(
        '%m/%d/%Y') + '\n\n' + 'Downloading Data for %s Stocks...\n' % count)

stocks = {s: yf.getHistoricData(
        s, start) for s in symbols} # fetch price data for given tickers
stocks = {s: tech.analyze(
        stocks[s]) for s in symbols} # append technical indicators

for s in symbols: # format date (index) column
    stocks[s]["Date"] = stocks[s].index.date
    stocks[s].set_index("Date", drop=True, inplace=True)

elapsed = dt.datetime.now() - now # calculate total execution time
print(('\n' 'Completed Successfully in %s') % elapsed)
  
close = pd.DataFrame({s: stocks[s]['adj_close'] for s in symbols})
price = {s: close.loc[:, s] for s in symbols}
close = close.dropna()
missing_cl = close.isna()
info = close.describe()

# normalize adjusted close price for all stocks (rescaled: 0-1)
low_cl = close.min()
lowest_cl = low_cl.min()
high_cl = close.max()
highest_cl = high_cl.max()
normalized = (close - lowest_cl) / (highest_cl - lowest_cl)
 
first_cl = {s: stocks[s]['adj_close'].
            head(1).transpose() for s in symbols} # first traded price within range
last_cl = close.tail(1).transpose() # last traded price within range

# calculate correlation, cummulative return & daily price change for each stock
daily_return = close.apply(lambda x: x / x[0])
stock_change = close.apply(lambda x: np.log(x) - np.log(x.shift(1)))
dataDiff = close.diff()[1:]
countPositive = dataDiff > 0
upDays = pd.DataFrame(countPositive.sum())
total_return = daily_return.tail(1).transpose()
corr = close.corr()

# create csv files for each stock
cwd = os.path.dirname(__file__)
for s in symbols:
    stocks[s].to_csv(cwd + '/dumps/' + s + '.csv')

# start plotting data
daily_return.plot(grid = True, title = 'Cummulative Return (Percent)', lw = .5
                  ).axhline(y = 1, color = "black", lw = 2)
stock_change.plot(grid = True, title = 'Price Change (Percent)', lw = .5
                  ).axhline(y = 0, color = "black", lw = 2)
stock_change.plot(grid = True, subplots=True, title = 
                  'Price Change (Percent)', lw = .5)
close.plot(grid = True, subplots=True, title = 'Adjusted Close (Price)', 
           lw = .5, layout=(int(count/2), 2))
close.plot(grid = True, title = 'Adjusted Close (Price)', lw = .5)
_, ax = plt.subplots() 
_ = sns.heatmap(corr, ax=ax, xticklabels=corr.columns.values, 
                yticklabels=corr.columns.values, cmap='coolwarm')
