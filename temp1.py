# -*- coding: utf-8 -*-
"""
Created on Mon Dec 19 11:13:28 2022

@author: bidzh
"""

from analytics.ratios import *
from analytics.value_at_risk import *
from dbupload.config import *


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

Stocks = ['IBM',  'ISIG']
Shares = [0.6, 0.4]



class StockDownload:
    def __init__(self, stockList):
        self.stockList = stockList
        
    def Download(self):
        PortfolioStocks = pd.DataFrame()
        
        for stock in self.stockList:
            time.sleep(20)
            print(stock)
            Query = {
                  'function': 'TIME_SERIES_DAILY_ADJUSTED'
                , 'symbol': stock
                , 'outputsize' : "full"
                , 'datatype': 'json'
                , 'apikey': API_KEY
                }
            response = re.get(url, params = Query)
            
            if response.status_code != 200:
                raise ValueError("The status code is {}. Consider revising code".format(response.status_code))
            print(response.json().keys())
            # StockDf = pd.DataFrame.from_dict(response.json()[dict_key]).T['4. close']
            StockDf = pd.DataFrame.from_dict(response.json()['Time Series (Daily)']).T['4. close']
            StockDf = pd.DataFrame(StockDf.astype(float))
            StockDf.columns = [stock]
            
            PortfolioStocks = pd.concat([PortfolioStocks, StockDf], axis = 1)
            PortfolioStocks = PortfolioStocks.sort_index(ascending=True)
            
        PortfolioStocks_pct = PortfolioStocks.apply(lambda x: np.log(x/x.shift(1))).dropna()
            
            # PortfolioStocks_pct = PortfolioStocks.pct_change().dropna()
            
        return PortfolioStocks_pct
    

class StockPortfolio:
    Portfolio_pct = None
    
    def __init__(self, stockList, sharesList, amount):
        self.stockList = stockList
        self.sharesList = sharesList
        self.amount = amount
        if StockPortfolio.Portfolio_pct is None:
            StockPortfolio.Portfolio_pct = self.StockDownload
            
    def StockDownload(self):
        
        PortfolioStocks = pd.DataFrame()
        
        for stock in self.stockList:
            time.sleep(20)
            print(stock)
            Query = {
                  'function': 'TIME_SERIES_DAILY_ADJUSTED'
                , 'symbol': stock
                , 'outputsize' : "full"
                , 'datatype': 'json'
                , 'apikey': API_KEY
                }
            response = re.get(url, params = Query)
            
            if response.status_code != 200:
                raise ValueError("The status code is {}. Consider revising code".format(response.status_code))
            print(response.json().keys())
            # StockDf = pd.DataFrame.from_dict(response.json()[dict_key]).T['4. close']
            StockDf = pd.DataFrame.from_dict(response.json()['Time Series (Daily)']).T['4. close']
            StockDf = pd.DataFrame(StockDf.astype(float))
            StockDf.columns = [stock]
            
            PortfolioStocks = pd.concat([PortfolioStocks, StockDf], axis = 1)
            PortfolioStocks = PortfolioStocks.sort_index(ascending=True)
            
        PortfolioStocks_pct = PortfolioStocks.apply(lambda x: np.log(x/x.shift(1))).dropna()
            
            # PortfolioStocks_pct = PortfolioStocks.pct_change().dropna()
            
        return PortfolioStocks_pct
        
    def Optimize(self):
        
        mu = expected_returns.ema_historical_return(Portfolio_pct
                                                    , returns_data = False # this meas
                                                    , compounding = False
                                                    , frequency = 252
                                                    , log_returns = True)
        S = risk_models.exp_cov(prices= Portfolio_pct
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

    def VaR(self, df, newShares):
        
        PortReturn = pd.DataFrame(np.matmul(df, newShares))
        PortReturn.columns = ['close_pc']
        VaR_uniform = FillVaR(PortReturn).astype(float)
        
        lastVaR_sum = (self.amount) * VaR_uniform[-1:]
        # lastVaR_sum = lastVaR_sum['Parametric EWMA'][0]
        lastVaR_sum = lastVaR_sum['Historical VaR'][0]
        
        return lastVaR_sum













