# -*- coding: utf-8 -*-
"""
Created on Sat Dec 17 11:09:23 2022

@author: bidzh
"""

from analytics.ratios import *
from analytics.value_at_risk import *
from dbupload.config import *
from get_stock import *

import requests as re
import pandas as pd
import numpy as np
import os 
from scipy.stats import norm
import matplotlib.pyplot as plt
import time
from pypfopt import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns

url = constant.url
API_KEY = constant.api_key

Stocks = ['AAPL', 'MSFT', 'AMZN', 'IBM',  'ISIG']

class VaR():
    """
        Этот класс считает VaR потрфеля. Для расчета он скачивает данные из API Alpha vantage.
        Метод который скачивает - StockDownload
    """
    
    def __init__(self, stock_list, shares_list, amount):
        self.stock_list = stock_list
        self.shares_list = shares_list
        self.amount = amount
        
    
    def VaRCalc(self):
        
        
        Portfolio = getStockBars(self.stock_list
                                 , TimeFrame.Day
                                 , start = pd.to_datetime('2010-01-01')
                                 , end = pd.to_datetime('2022-12-20'))  # вот скачивает данные
        Portfolio.index = Portfolio['date']
        Portfolio = Portfolio.drop(columns = ['date'])
        Portfolio_pct = Portfolio.apply(lambda x: np.log(x/x.shift(1))).dropna()
        
        # =============================================================================
        # VaR with uniform distribution  
        # =============================================================================
        
        # init_shares = [1/len(self.stock_list) for i in range(len(self.stock_list))]
        init_shares = self.shares_list
        PortReturn = pd.DataFrame(np.matmul(Portfolio_pct, init_shares))
        PortReturn.columns = ['close_pc']
        VaR_uniform = FillVaR(PortReturn).astype(float)
        
        lastVaR_sum = (self.amount) * VaR_uniform[-1:]
        # lastVaR_sum = lastVaR_sum['Parametric EWMA'][0]
        lastVaR_sum = lastVaR_sum['Historical VaR'][0]
        
        return lastVaR_sum



# a = VaR(Stocks, [0.2, 0.2, 0.2, 0.2, 0.2], 1000).VaRCalc()
        
        
class OptimizePortfolio:
    """
        Этот класс рассчитывает оптимальные веса. Для рассчета оптимальных весов класс скаичвает данные из API Alpha vantage
    """
    
    def __init__(self, stock_list):
        self.stock_list = stock_list
        
 
        
    def Optimize(self):
        
        Portfolio = getStockBars(self.stock_list
                                 , TimeFrame.Day
                                 , start = pd.to_datetime('2010-01-01')
                                 , end = pd.to_datetime('2022-12-20'))
        Portfolio.index = Portfolio['date']
        Portfolio = Portfolio.drop(columns = ['date'])

        Portfolio_pct = Portfolio.apply(lambda x: np.log(x/x.shift(1))).dropna()
        
        mu = expected_returns.ema_historical_return(Portfolio
                                                    , returns_data = False # this meas
                                                    , compounding = False
                                                    , frequency = 252
                                                    , log_returns = True)
        S = risk_models.exp_cov(prices= Portfolio
                                , returns_data = False
                                , span = 180
                                , frequency = 252
                                , log_returns = True)
        
        # Optimize for maximal Sharpe ratio
        ef = EfficientFrontier(mu, S)
        raw_weights = ef.max_sharpe()
        new_weights = ef.clean_weights()        
        # print(cleaned_weights)
        pf = ef.portfolio_performance(verbose=True)
        
        
        # delete stocks with 0 weight
        for key, value in dict(new_weights).items():
            if value == 0:
                del new_weights[key]
                Portfolio_pct = Portfolio_pct.drop(key, axis = 1)
        
        return new_weights, Portfolio_pct
        
    
class StockPortfolio:
    def __init__(self, stock_list, amount):
        self.stock_list = stock_list
        self.amount = amount
        
    def info(self):
        
        NewStocks = OptimizePortfolio(self.stock_list).Optimize()    # в этом коде скачиваются            
        
        OptimizedStockList = list(NewStocks[0].keys()) 
        OptimizedSharesList = list(NewStocks[0].values()) 
        OptimizedAmount = [round(i* self.amount, 2) for i in OptimizedSharesList]
        
        NewData = NewStocks[1]
        
        finalData = pd.DataFrame(list(zip(OptimizedStockList, OptimizedSharesList, OptimizedAmount))
                                  , columns = ['Ticker', 'Share', 'Amount'])
    
    
        VaRPortfolio = VaR(OptimizedSharesList, OptimizedStockList, self.amount) #insert new stockss list
        
        VaRSum = VaRPortfolio.VaRCalc() # и здесь тоже рассчитываются
        
        
        Portfolio_pct = NewStocks[1]
        
        # Margin & Component VaR section ---------------------
        finalVaR = pd.DataFrame()
        if len(OptimizedSharesList) > 1:
            margVaR = [MarginVaR(i, Portfolio_pct, OptimizedSharesList) for i in OptimizedStockList] 
            margVaR_df = pd.DataFrame(margVaR, OptimizedStockList)
            margVaR_df.columns = ['MarginVaR']
            
            finalVaR = margVaR_df.join(new_weights)
            finalVaR['ComponentVaR'] = finalVaR['MarginVaR'] * finalVaR['shares']*lastVaR_sum_opt
        
        else:
            margVaR = pd.DataFrame()
            
        return finalVaR, finalData
        
        
        
        
a = OptimizePortfolio(Stocks)    
b = a.Optimize()        
list(b[0].keys())
list(b[0].values())   

[round(i*1000, 2) for i in list(b[0].values())]

c = b[1]      
        
        
v = StockPortfolio(Stocks, 1000) 
v1 = v.info()
v2 = v.info()        
        
        
        