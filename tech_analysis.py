# -*- coding: utf-8 -*-

# tech_analysis.py

import numpy as np, pandas as pd # data analysis and wrangling
from scipy.stats import norm # statistical functions

def analyze(df):
#Simple Moving Average (SMA)
    df["SMA20d"] = np.round(df["adj_close"].rolling(window = 20, center = False).mean(), 2)
    df["SMA50d"] = np.round(df["adj_close"].rolling(window = 50, center = False).mean(), 2)
    df["SMA200d"] = np.round(df["adj_close"].rolling(window = 200, center = False).mean(), 2)
    df['SMA20d-SMA50d'] = (df['SMA20d'] - df['SMA50d'])
    
#Exponential Moving Average (EMA)
    df["EMA10d"] = pd.Series.ewm(df['adj_close'], ignore_na=True,span=10,min_periods=9,adjust=True).mean()
    df["EMA50d"] = pd.Series.ewm(df['adj_close'], ignore_na=False,span=50,min_periods=49,adjust=True).mean()
    df["EMA100d"] = pd.Series.ewm(df['adj_close'], ignore_na=False,span=100,min_periods=99,adjust=True).mean()
    
#Bollinger Bands (BB)
    df["STD20d"] = pd.Series.rolling(df['adj_close'],window=20,center=False).std()
    df['Bollinger Band(+)'] = df["SMA20d"] + 2 * df["STD20d"]
    df['Bollinger Band(-)'] = df["SMA20d"] - 2 * df["STD20d"]
    df["B1"] = 4 * df["STD20d"] / df["SMA20d"]
    df["B2"] = (df['adj_close'] - df["SMA20d"] + 2 * df["STD20d"]) / (4 * df["STD20d"])
    df["%B"] = (df['adj_close'] - df['Bollinger Band(-)']) / (df['Bollinger Band(+)'] - df['Bollinger Band(-)'])
    
#Momentum (MOM)
    df["MOM"] = df['adj_close'].diff(10)
    
#Rate of Change (RoC)
    M = df['adj_close'].diff(10 - 1)
    N = df['adj_close'].shift(10 - 1)
    df["RoC"] = M / N
    
#Stochastic Oscillator %K (SO%k)
    df["SO%k"] = (df['adj_close'] - df['low']) / (df['high'] - df['low'])
    
#Stochastic Oscillator %D (SO%d)
    df["SO%d"] = pd.Series.ewm( df["SO%k"],ignore_na=False,span=10,min_periods=9,adjust=True).mean()
    
#Mass Index (MX)
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
    
#Force Index (FX)
    df["ForceIndex"] = pd.Series(df['adj_close'].diff(10) * df['volume'].diff(10), name = 'force' + str(10))
    
#Ease of Movement (EoM)
    df["EoM"] = (df['high'].diff(1) + df['low'].diff(1)) * (df['high'] - df['low']) / (2 * df['volume'])
    df["EoM_Ma"] = pd.Series.rolling(df["EoM"], window=10,center=False).mean()
    
#Commodity Channel Index (CCI)
    df["PP"] = (df['high'] + df['low'] + df['adj_close']) / 3
    df["CCI"] = pd.Series((df["PP"] - pd.Series.rolling(df["PP"], window=20,center=False).mean()) / pd.Series.rolling(df["PP"], window=20,center=False).std())   
    
#Coppock Curve (CoppCurve)
    M1 = df['adj_close'].diff(int(20 * 11 / 10) - 1)
    N1 = df['adj_close'].shift(int(20 * 11 / 10) - 1)
    ROC1 = M1 / N1
    M2 = df['adj_close'].diff(int(20 * 14 / 10) - 1)
    N2 = df['adj_close'].shift(int(20 * 14 / 10) - 1)
    ROC2 = M2 / N2
    df['CoppCurve'] = pd.Series.ewm(ROC1 + ROC2, ignore_na=False,span=20,min_periods=20,adjust=True).mean()
    
#Keltner Channel (KelCh)
    df['KelChM'] = pd.Series.rolling((df['high'] + df['low'] + df['adj_close']) / 3, window=10,center=False).mean()
    df['KelChU'] = pd.Series.rolling((4 * df['high'] - 2 * df['low'] + df['adj_close']) / 3, window=10,center=False).mean()
    df['KelChD'] = pd.Series.rolling((-2 * df['high'] + 4 * df['low'] + df['adj_close']) / 3, window=10,center=False).mean()    
    
#Chaikin Oscillator (CO)
    df['ADL'] = (2 * df['adj_close'] - df['high'] - df['low']) / (df['high'] - df['low']) * df['volume']
    df['Chaikin'] = pd.Series.ewm(df['ADL'], ignore_na=False,span=3,min_periods=2,adjust=True).mean() - pd.Series.ewm(df['ADL'], ignore_na=False,span=10,min_periods=9,adjust=True).mean()
    
#Value at Risk (VaR)
    P = 1e6   # 1,000,000 USD
    c = 0.99  # 99% confidence interval
    df["rets"] = df["adj_close"].pct_change()
    mu = np.mean(df["rets"])
    sigma = np.std(df["rets"])
    alpha = norm.ppf(1-c, mu, sigma)
    df['VaR'] = P - P*(alpha + 1)
    
"""
#Average True Range (ATR)
    i = 0
    TR_l = [0]
    while i < df.index[-1]:
        TR = max(df.get_value(i + 1, df['high']), df.get_value(i, df['adj_close'])) - min(df.get_value(i + 1, df['low']), df.get_value(i, df['adj_close']))
        TR_l.append(TR)
        i = i + 1
        TR_s = pd.Series(TR_l)
    df["ATR"] = pd.ewma(TR_s, span = 10, min_periods = 10) 
	
#Donchian Channel (DonCh)
    i = 0
    DC_l = []
    while i < 10 - 1:
        DC_l.append(0)
        i = i + 1
    i = 0
    while i + 10 - 1 < df.index[-1]:
        DC = max(df['high'].ix[i:i + 10 - 1]) - min(df['low'].ix[i:i + 10 - 1])
        DC_l.append(DC)
        i = i + 1
    df['DonCh'] = pd.Series(DC_l, name = 'Donchian' + str(10))
    df['DonCh'] = df['DonCh'].shift(10 - 1)   
	
#Ultimate Oscillator (UltO)
    i = 0
    TR_l = [0]
    BP_l = [0]
    while i < df.index[-1]:
        TR = max(df.get_value(i + 1, df['high']), df.get_value(i, df['adj_close'])) - min(df.get_value(i + 1, df['low']), df.get_value(i, df['adj_close']))
        TR_l.append(TR)
        df['BP'] = df.get_value(i + 1, df['adj_close']) - min(df.get_value(i + 1, df['low']), df.get_value(i, df['adj_close']))
        BP_l.append(df['BP'])
        i = i + 1
    df['UltO'] = pd.Series((4 * pd.rolling_sum(pd.Series(BP_l), 7) / pd.rolling_sum(pd.Series(TR_l), 7)) + (2 * pd.rolling_sum(pd.Series(BP_l), 14) / pd.rolling_sum(pd.Series(TR_l), 14)) + (pd.rolling_sum(pd.Series(BP_l), 28) / pd.rolling_sum(pd.Series(TR_l), 28)), name = 'Ultimate Osc')

#Pivot Points, Supports and Resistances (PSR)
    df["PP"] = pd.Series((df['high'] + df['low'] + df['adj_close']) / 3)
    df["R1"] = pd.Series(2 * df["PP"] - df['low'])
    df["S1"] = pd.Series(2 * df["PP"] - df['high'])
    df["R2"] = pd.Series(df["PP"] + df['high'] - df['low'])
    df["S2"] = pd.Series(df["PP"] - df['high'] + df['low'])
    df["R3"] = pd.Series(df['high'] + 2 * (df["PP"] - df['low']))
    df["S3"] = pd.Series(df['low'] - 2 * (df['high'] - df["PP"]))
    df["PSR"] = pd.DataFrame({'PP':df["PP"], 'R1':df["R1"], 'S1':df["S1"], 'R2':df["R2"], 'S2':df["S2"], 'R3':df["R3"], 'S3':df["S3"]})

#Triple Exponential Moving Average Oscillator (TRIX)
    ex1 = pd.ewma(df['adj_close'], span = 9, min_periods = 9 - 1)
    ex2 = pd.ewma(ex1, span = 12, min_periods = 12 - 1)
    ex3 = pd.ewma(ex2, span = 26, min_periods = 26 - 1)
    i = 0
    ROC_1 = [0]
    while i + 1 <= df.index[-1]:
        ROC = (ex3[i + 1] - ex3[i]) / ex3[i]
        ROC_1.append(ROC)
        i = i + 1
    df["TRIX"] = pd.Series(ROC_1, name = 'TRIX' + str(26)) 

#Average Directional Movement Index (ADX)
    i = 0
    UpI = []
    DoI = []
    while i + 1 <= df.index[-1]:
        UpMove = df.get_value(i + 1, df['high']) - df.get_value(i, df['high'])
        DoMove = df.get_value(i, df['low']) - df.get_value(i + 1, df['low'])
        if UpMove > DoMove and UpMove > 0:
            UpD = UpMove
        else: UpD = 0
        UpI.append(UpD)
        if DoMove > UpMove and DoMove > 0:
            DoD = DoMove
        else: DoD = 0
        DoI.append(DoD)
        i = i + 1
    i = 0
    TR_l = [0]
    while i < df.index[-1]:
        TR = max(df.get_value(i + 1, df['high']), df.get_value(i, df['adj_close'])) - min(df.get_value(i + 1, df['low']), df.get_value(i, df['adj_close']))
        TR_l.append(TR)
        i = i + 1
    TR_s = pd.Series(TR_l)
    ATR = pd.Series(pd.ewma(TR_s, span = 14, min_periods = 14))
    UpI = pd.Series(UpI)
    DoI = pd.Series(DoI)
    PosDI = pd.Series(pd.ewma(UpI, span = 14, min_periods = 14 - 1) / ATR)
    NegDI = pd.Series(pd.ewma(DoI, span = 14, min_periods = 14 - 1) / ATR)
    df['ADX'] = pd.Series(pd.ewma(abs(PosDI - NegDI) / (PosDI + NegDI), span = 14, min_periods = 14 - 1), name = 'ADX' + str(14) + '_' + str(14))

#Vortex Indicator (VI)
    i = 0
    df['TR'] = [0]
    while i < df.index[-1]:
        Range = max(df.get_value(i + 1, df['high']), df.get_value(i, df['adj_close'])) - min(df.get_value(i + 1, df['low']), df.get_value(i, df['adj_close']))
        df['TR'].append(Range)
        i = i + 1
    i = 0
    df['VM'] = [0]
    while i < df.index[-1]:
        Range = abs(df.get_value(i + 1, df['high']) - df.get_value(i, df['low'])) - abs(df.get_value(i + 1, df['low']) - df.get_value(i, df['high']))
        df['VM'].append(Range)
        i = i + 1
    df['VI'] = pd.Series(pd.rolling_sum(pd.Series(df['VM']), 14) / pd.rolling_sum(pd.Series(df['TR']), 14), name = 'Vortex' + str(14))

#Know Sure Thing (KST Oscillator)
    M = df['adj_close'].diff(10 - 1)
    N = df['adj_close'].shift(10 - 1)
    ROC1 = M / N
    M = df['adj_close'].diff(10 - 1)
    N = df['adj_close'].shift(10 - 1)
    ROC2 = M / N
    M = df['adj_close'].diff(10 - 1)
    N = df['adj_close'].shift(10 - 1)
    ROC3 = M / N
    M = df['adj_close'].diff(15 - 1)
    N = df['adj_close'].shift(15 - 1)
    ROC4 = M / N
    df['KST'] = pd.Series(pd.rolling_sum(ROC1, 10) + pd.rolling_sum(ROC2, 15) * 2 + pd.rolling_sum(ROC3, 20) * 3 + pd.rolling_sum(ROC4, 30) * 4, name = 'KST' + str(10) + '_' + str(10) + '_' + str(10) + '_' + str(15) + '_' + str(10) + '_' + str(15) + '_' + str(20) + '_' + str(30))
	df['KSTsignal'] = np.round(df['KST'].rolling(window = 9, center = False).mean(), 2)

#Relative Strength Index (RSI)
    i = 0
    UpI = [0]
    DoI = [0]
    while i + 1 <= df.index[-1]:
        UpMove = df.get_value(i + 1, df['high']) - df.get_value(i, df['high'])
        DoMove = df.get_value(i, df['low']) - df.get_value(i + 1, df['low'])
        if UpMove > DoMove and UpMove > 0:
            UpD = UpMove
        else: UpD = 0
        UpI.append(UpD)
        if DoMove > UpMove and DoMove > 0:
            DoD = DoMove
        else: DoD = 0
        DoI.append(DoD)
        i = i + 1
    UpI = pd.Series(UpI)
    DoI = pd.Series(DoI)
    PosDI = pd.Series(pd.ewma(UpI, span = 14, min_periods = 14 - 1))
    NegDI = pd.Series(pd.ewma(DoI, span = 14, min_periods = 14 - 1))
    df['RSI'] = pd.Series(PosDI / (PosDI + NegDI), name = 'RSI' + str(14))

#True Strength Index (TSI)
    M = pd.Series(df['adj_close'].diff(1))
    aM = abs(M)
    EMA1 = pd.Series(pd.ewma(M, span = 25, min_periods = 25 - 1))
    aEMA1 = pd.Series(pd.ewma(aM, span = 25, min_periods = 25 - 1))
    EMA2 = pd.Series(pd.ewma(EMA1, span = 13, min_periods = 13 - 1))
    aEMA2 = pd.Series(pd.ewma(aEMA1, span = 13, min_periods = 13 - 1))
    df['TSI'] = pd.Series(EMA2 / aEMA2, name = 'TSI' + str(25) + '_' + str(13))

#Accumulation/Distribution (AD)
    df['AD'] = (2 * df['adj_close'] - df['high'] - df['low']) / (df['high'] - df['low']) * df['volume']
	ad = df['AD']
    M = ad.diff(10 - 1)
    N = ad.shift(10 - 1)
    ROC = M / N
    df['AD_ROC'] = pd.Series(ROC, name = 'Acc/Dist_RoC' + str(10))

#On-balance Volume (OBV)
    i = 0
    df['OBV'] = [0]
	OBV = df['OBV']
    while i < df.index[-1]:
        if df.get_value(i + 1, df['adj_close']) - df.get_value(i, df['adj_close']) > 0:
            OBV.append(df.get_value(i + 1, df['volume']))
        if df.get_value(i + 1, df['adj_close']) - df.get_value(i, df['adj_close']) == 0:
            OBV.append(0)
        if df.get_value(i + 1, df['adj_close']) - df.get_value(i, df['adj_close']) < 0:
            OBV.append(-df.get_value(i + 1, df['volume']))
        i = i + 1
    OBV = pd.Series(OBV)
    df['OBV_MA'] = pd.Series(pd.rolling_mean(OBV, 10), name = 'OBV' + str(10))
 """

    return df
