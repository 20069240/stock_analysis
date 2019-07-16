# -*- Python 2.7.14 -*-
# -*- coding: utf-8 -*-
# -*- Spyder Editor -*-

"""Created by Adrian Aley on Mon Dec 04 03:54:50 2017"""

# mymodules.py
__author__ = 'adrian'

import sys, matplotlib.pyplot as plt, matplotlib.dates as mdates, \
pandas_datareader as pdr, pandas as pd, numpy as np, datetime as dt
from mpl_finance import candlestick_ohlc
from scipy.stats import norm

# -------------------------- create dictionary with several lookback periods
today = dt.date.today()
past = {'1month':[today - dt.timedelta(days=31)],
        '3months':[today - dt.timedelta(days=90)],
        '6months':[today - dt.timedelta(days=182)],
        '9months':[today - dt.timedelta(days=274)],
        '1year':[dt.date(today.year - 1, today.month, today.day)],
        '3years':[dt.date(today.year - 3, today.month, today.day)],
        '5years':[dt.date(today.year - 5, today.month, today.day)],
        '10years':[dt.date(today.year - 10, today.month, today.day)]}

def time_format(secs):
    mins,secs=divmod(secs,60)
    hours,mins=divmod(mins, 60)
    return '%02d:%02d' % (mins, secs)

def var_cov_var(P, c, mu, sigma):
    """Variance-Covariance calculation of daily Value-at-Risk
    using confidence level c, with mean of returns mu and 
    standard deviation of returns sigma, on a portfolio of value P."""
    alpha = norm.ppf(1-c, mu, sigma)
    return P - P*(alpha + 1)

def value_at_risk(data, P="", c="", mu="", sigma=""):
    P = 1e6   # 1,000,000 USD
    c = 0.99  # 99% confidence interval
    data["rets"] = data["adj_close"].pct_change()    
    mu = np.mean(data["rets"])
    sigma = np.std(data["rets"])  
    var = var_cov_var(P, c, mu, sigma)     
    return var

def printer(data):
    sys.stdout.write("\r\x1b[K"+data.__str__())
    sys.stdout.flush()
    
def print_all(l):
   for i in l:
      if isinstance(i,list):
         print_all(i)
      else:
         print(i)     
         
def get(tickers, startdate, enddate):
  def data(ticker):
    return (pdr.get_data_yahoo(ticker, start=startdate, end=enddate))
  datas = map (data, tickers)
  return(pd.concat(datas, keys=tickers, names=['Ticker', 'Date']))
  
def plot_candlestick(df, ax=None, title=None, fmt='%x'):
    """Plots a candlestick chart of dataframe object"""
    if ax is None:
        fig, ax = plt.subplots()
        fig.tight_layout()
    idx_name = df.index.name
    dat = df.reset_index()[[idx_name, "open", "high", "low", "close"]]
    dat[df.index.name] = dat[df.index.name].map(mdates.date2num)       
    ax.xaxis_date()
    ax.xaxis.set_major_formatter(mdates.DateFormatter(fmt))
    plt.xticks(rotation=45)
    _ = candlestick_ohlc(ax, dat.values, width=.6, colorup='g', alpha =1)
    ax.set_title(title)
    return ax