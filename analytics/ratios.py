# -*- coding: utf-8 -*-
"""
Created on Wed Dec 14 11:52:32 2022

@author: bidzh
"""


import pandas as pd
import numpy as np
import os 
from scipy.stats import norm
from pypfopt import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns



# =============================================================================
# functions
# =============================================================================

def SharpeRatio(return_series, N, rf = 0.01):
    """
        inputs:
            return_series: Portfolio return
            N:             N days
            rf:            Risk-free rate
            
        Output: Sharp ratio
    """
    mean = return_series.mean() * N -rf
    sigma = return_series.std() * np.sqrt(N)
    
    return round(mean / sigma, 4)


def SortinoRatio(series, N, rf = 0.01):
    """
        inputs: 
            series: return series of asset
            N:      N days
            rf:     Risk-free rate
        
        output: Sortino Ratio
    """
    mean = series.mean() * N -rf
    std_neg = series[series<0].std()*np.sqrt(N)
    return round(mean/std_neg, 4)
