# -*- coding: utf-8 -*-
"""
Created on Sun Dec 25 19:47:33 2022

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
from typing import Optional, Union



def VaRCalc(symbols: Union[str, list[str]]
            , shares: Union[float, list[float]]
            , amount: int = 1000):
    
    """
        Calculates the Value-at-Risk of a given portfolio or single assets
    """
    
    if len(symbols) == 1:
        shares = [1]
      
    Portfolio = getStockBars(symbols
                             , start = pd.to_datetime('2015-01-01')
                             , end = pd.to_datetime('2022-12-23'))
    Portfolio.index = Portfolio['date']
    Portfolio = Portfolio.drop(columns = ['date'])
    
    Portfolio_pct = Portfolio.apply(lambda x: np.log(x/x.shift(1))).dropna()
    
    PortReturn = pd.DataFrame(np.matmul(Portfolio_pct, shares))
    PortReturn.columns = ['close_pc']
    
    VaR = FillVaR(PortReturn).astype(float)
    
    lastVaR_sum = amount * VaR[-1:]
    # lastVaR_sum = lastVaR_sum['Parametric EWMA'][0]
    lastVaR_sum = lastVaR_sum['Historical VaR'][0]
      
    
    return lastVaR_sum, VaR[-1:]
    

data = VaRCalc(['IBM', 'MSFT', 'AAPL'], [0.4, 0.4, 0.2])
    

def Optimize(symbols: Union[str, list[str]]):
    """
        The function gets an optimized stock weights
    """
    
    if len(symbols) == 1:
        return 1
    
    Portfolio = getStockBars(symbols
                             , start = pd.to_datetime('2015-01-01')
                             , end = pd.to_datetime('2022-12-23'))
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
    
    
    
    
opt = Optimize(['IBM', 'MSFT', 'AAPL', 'ISIG', 'AMZN', 'TSLA'])
    

# def StockPortfolio(symbols: Union[str, list[str]]
#                    , amount: int = 1000):
    
    
    
    
    
    
    
    
    
    
    
    