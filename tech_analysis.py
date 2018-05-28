# -*- coding: utf-8 -*-

# tech_analysis.py

import numpy as np, pandas as pd # data analysis and wrangling
from scipy.stats import norm # statistical functions

def analyze(df):
#Simple Moving Average
    df["SMA20d"] = np.round(df["adj_close"].rolling(window = 20, center = False).mean(), 2)
    df["SMA50d"] = np.round(df["adj_close"].rolling(window = 50, center = False).mean(), 2)
    df["SMA200d"] = np.round(df["adj_close"].rolling(window = 200, center = False).mean(), 2)
    df['SMA20d-SMA50d'] = (df['SMA20d'] - df['SMA50d'])
    
#Exponential Moving Average
    df["EMA10d"] = pd.Series.ewm(df['adj_close'], ignore_na=True,span=10,min_periods=9,adjust=True).mean()
    df["EMA50d"] = pd.Series.ewm(df['adj_close'], ignore_na=False,span=50,min_periods=49,adjust=True).mean()
    df["EMA100d"] = pd.Series.ewm(df['adj_close'], ignore_na=False,span=100,min_periods=99,adjust=True).mean()
    
#Bollinger Bands 
    df["STD20d"] = pd.Series.rolling(df['adj_close'],window=20,center=False).std()
    df['Bollinger Band(+)'] = df["SMA20d"] + 2 * df["STD20d"]
    df['Bollinger Band(-)'] = df["SMA20d"] - 2 * df["STD20d"]
    df["B1"] = 4 * df["STD20d"] / df["SMA20d"]
    df["B2"] = (df['adj_close'] - df["SMA20d"] + 2 * df["STD20d"]) / (4 * df["STD20d"])
    df["%B"] = (df['adj_close'] - df['Bollinger Band(-)']) / (df['Bollinger Band(+)'] - df['Bollinger Band(-)'])
    
#Momentum
    df["MOM"] = df['adj_close'].diff(10)
    
#Rate of Change
    M = df['adj_close'].diff(10 - 1)
    N = df['adj_close'].shift(10 - 1)
    df["RoC"] = M / N
    
#Stochastic oscillator %K
    df["SO%k"] = (df['adj_close'] - df['low']) / (df['high'] - df['low'])
    
#Stochastic oscillator %D
    df["SO%k"] = (df['adj_close'] - df['low']) / (df['high'] - df['low'])
    df["SO%d"] = pd.Series.ewm( df["SO%k"],ignore_na=False,span=10,min_periods=9,adjust=True).mean()
    
#Mass Index
    Range = df['high'] - df['low']
    EX1 = pd.Series.ewm(Range, ignore_na=False,span=9,min_periods=8,adjust=True).mean()
    EX2 = pd.Series.ewm(EX1, ignore_na=False,span=9,min_periods=8,adjust=True).mean()
    df["Mass"] = EX1 / EX2
    df["Mass Index"] = pd.Series.rolling(df["Mass"], window=25,center=False).sum()
    
#MACD, MACD Signal and MACD difference
    EMAfast = pd.Series.ewm(df['adj_close'], ignore_na=False,span=9,min_periods=25,adjust=True).mean()
    EMAslow = pd.Series.ewm(df['adj_close'], ignore_na=False,span=26,min_periods=25,adjust=True).mean()
    df["MACD"] = pd.Series(EMAfast - EMAslow, name = 'MACD' + str(9) + '_' + str(26))
    df["MACDsign"] = pd.Series.ewm(df["MACD"], ignore_na=False,span=9,min_periods=8,adjust=True).mean()
    df["MACDdiff"] = pd.Series(df["MACD"] - df["MACDsign"], name = 'MACDdiff' + str(9) + '_' + str(26))
    
#Force Index
    df["ForceIndex"] = pd.Series(df['adj_close'].diff(10) * df['volume'].diff(10), name = 'force' + str(10))
    
#Ease of Movement
    df["EoM"] = (df['high'].diff(1) + df['low'].diff(1)) * (df['high'] - df['low']) / (2 * df['volume'])
    df["EoM_Ma"] = pd.Series.rolling(df["EoM"], window=10,center=False).mean()
    
#Commodity Channel Index
    df["PP"] = (df['high'] + df['low'] + df['adj_close']) / 3
    df["CCI"] = pd.Series((df["PP"] - pd.Series.rolling(df["PP"], window=20,center=False).mean()) / pd.Series.rolling(df["PP"], window=20,center=False).std())   
    
#Coppock Curve
    M1 = df['adj_close'].diff(int(20 * 11 / 10) - 1)
    N1 = df['adj_close'].shift(int(20 * 11 / 10) - 1)
    ROC1 = M1 / N1
    M2 = df['adj_close'].diff(int(20 * 14 / 10) - 1)
    N2 = df['adj_close'].shift(int(20 * 14 / 10) - 1)
    ROC2 = M2 / N2
    df['CoppCurve'] = pd.Series.ewm(ROC1 + ROC2, ignore_na=False,span=20,min_periods=20,adjust=True).mean()
    
#Keltner Channel
    df['KelChM'] = pd.Series.rolling((df['high'] + df['low'] + df['adj_close']) / 3, window=10,center=False).mean()
    df['KelChU'] = pd.Series.rolling((4 * df['high'] - 2 * df['low'] + df['adj_close']) / 3, window=10,center=False).mean()
    df['KelChD'] = pd.Series.rolling((-2 * df['high'] + 4 * df['low'] + df['adj_close']) / 3, window=10,center=False).mean()    
    
#Chaikin Oscillator
    df['ADL'] = (2 * df['adj_close'] - df['high'] - df['low']) / (df['high'] - df['low']) * df['volume']
    df['Chaikin'] = pd.Series.ewm(df['ADL'], ignore_na=False,span=3,min_periods=2,adjust=True).mean() - pd.Series.ewm(df['ADL'], ignore_na=False,span=10,min_periods=9,adjust=True).mean()
    
# Value at Risk
    P = 1e6   # 1,000,000 USD
    c = 0.99  # 99% confidence interval
    df["rets"] = df["adj_close"].pct_change()
    mu = np.mean(df["rets"])
    sigma = np.std(df["rets"])
    alpha = norm.ppf(1-c, mu, sigma)
    df['VaR'] = P - P*(alpha + 1)  
    return df
