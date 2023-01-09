# -*- coding: utf-8 -*-
"""
Created on Wed Dec 14 16:03:53 2022

@author: bidzh
"""

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

from analytics.ratios import *
from analytics.value_at_risk import *
from dbupload.config import *


Stocks = ['AAPL', 'MSFT', 'AMZN', 'IBM',  'ISIG']
Comp_name = ['Apple', 'Microsoft', 'Amazon', 'IBM']
Shares = [0.2, 0.2, 0.2, 0.2, 0.2]

url = constant.url
API_KEY = constant.api_key


news_sources = ['cnn.com'
                , 'nytimes.com/international/section/us'
                , 'huffpost.com'
                , 'foxnews.com'
                , 'usatoday.com'
                , 'politico.com'
                , 'npr.org/sections/news/'
                , 'nydailynews.com']

class StockPortfolio:
    
    def __init__(self, stock_list, shares_list, amount, compName, sources = news_sources):
        self.stock_list = stock_list
        self.shares_list = shares_list
        self.amount = amount
        self.compName = compName
        self.sources = sources
    
    # def __setattr__(self, name, value):
    #     print(f">>> You set {name} = {value}")

   
    def StockDownload(self, TimeFrame = 'weekly'):
        
        url = 'https://www.alphavantage.co/query'
        API_KEY = 'IHGO514P7E4X0K30'
        
        # if TimeFrame == 'weekly':
        #     function = 'TIME_SERIES_WEEKLY'
        #     dict_key = 'Weekly Time Series'
        # elif TimeFrame == 'daily':
        #     function = 'TIME_SERIES_DAILY'
        
        PortfolioStocks = pd.DataFrame()
        
        for stock in self.stock_list:
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
            
            # PortfolioStocks_pct = PortfolioStocks.pct_change().dropna()
            
        return PortfolioStocks
    
    
    def PortfolioVaR(self):
        
        Portfolio = self.StockDownload()
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
        
        # =============================================================================
        # Portfolio Optimization by Sharp Ratio    
        # =============================================================================
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
        
        
        # =============================================================================
        # VaR of Optimized Portfolio  
        # =============================================================================
       
        # переделать 
        new_weights_ordered = [new_weights[i] for i in self.stock_list if i in new_weights.keys()]
        
        # calculcate 
        PortReturn_opt = pd.DataFrame(np.matmul(Portfolio_pct, new_weights_ordered))
        PortReturn_opt.columns = ['close_pc']
        VaR_opt = FillVaR(PortReturn_opt).astype(float)
        
        lastVaR_sum_opt = (self.amount) * VaR_opt[-1:]
        # lastVaR_sum_opt = lastVaR_sum_opt['Parametric EWMA'][0]
        lastVaR_sum_opt = lastVaR_sum_opt['Historical VaR'][0]
        
        new_weights = pd.DataFrame(list(new_weights.values()), list(new_weights.keys()))
        new_weights.columns = ['shares']
        
        # final data 
        finalVaR = pd.DataFrame()
        
        # Marginal VaR
        if len(new_weights) > 1:            
            final_stocks = list(new_weights.index)
            margVaR = [MarginVaR(i, Portfolio_pct, list(new_weights['shares'])) for i in final_stocks] 
            margVaR_df = pd.DataFrame(margVaR, final_stocks)
            margVaR_df.columns = ['MarginVaR']
            
            finalVaR = margVaR_df.join(new_weights)
            finalVaR['ComponentVaR'] = finalVaR['MarginVaR'] * finalVaR['shares']*lastVaR_sum_opt
        
        else:
            margVaR = pd.DataFrame()
        
        return lastVaR_sum, new_weights, pf, lastVaR_sum_opt, Portfolio_pct, finalVaR, VaR_opt 
    

        

    
    
    
    
    
a = StockPortfolio(Stocks, Shares, 1000, Comp_name)    

b = a.StockDownload()    
    
c = a.PortfolioVaR()
    
    
    
    
    
    
    
    
    
    