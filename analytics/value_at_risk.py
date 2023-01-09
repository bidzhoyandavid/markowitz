# -*- coding: utf-8 -*-
"""
Created on Wed Dec 14 11:52:59 2022

@author: bidzh
"""


import pandas as pd
import numpy as np
import os 
from scipy.stats import norm
from pypfopt import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns
from typing import Optional, Union


# =============================================================================
# functions
# =============================================================================

def DelNa(Data):
    """ drops rows of df where all values are any
    """
    return Data.dropna(how='all')


def VaRCalculation(Data, Formula, Period_Interval,  Confidence_Interval = 0.99, EWMA_lambda = 0.94):
    """ Calculates Value-at-Risk using three methods
        1. Historical simulation
        2. Parametric VaR
        3. Parametric EWMA
    """
    
    # ===================================================
    # Historical simulation
    # ===================================================
    if Formula == 'Historical simulation':
        VaR = np.quantile(Data, 1 - Confidence_Interval)
        return(VaR)
    
    # ===================================================
    # Parametric Normal
    # ===================================================
    if Formula == 'Parametric Normal':
        VaR = Data.mean() - Data.std() * norm.ppf(Confidence_Interval)
        return(VaR)
   
    
    # ===================================================
    # Parametric EWMA
    # ===================================================
    if Formula == 'Parametric EWMA':
        Degree_of_Freedom = np.empty([Period_Interval, ])
        Weights =  np.empty([Period_Interval, ])
        Degree_of_Freedom[0] = 1
        Degree_of_Freedom[1] = EWMA_lambda
        Range = range(Period_Interval)
        for i in range(2,Period_Interval):
            Degree_of_Freedom[i]=Degree_of_Freedom[1]**Range[i]
        for i in range(Period_Interval):
            Weights[i]=Degree_of_Freedom[i]/sum(Degree_of_Freedom)           
        
        sqrdData = Data**2
        EWMAstd = np.sqrt(sum(Weights * sqrdData))
        
        VaR = Data.mean() - EWMAstd * norm.ppf(Confidence_Interval)
        return(VaR)

def FillVaR(Data, Period_Interval = 50):
    """
    calculates Vale-at-Risk for the wghole range of data
    Input:
        Data with portfolio returns
    Output:
        Data with portfolio returns and VaRs
    """
    Data = Data.sort_index(ascending = True)
    Data = DelNa(Data)
    # Data = pd.DataFrame(Data)
    
    Data['Historical VaR'] = ''
    Data['Parametric VaR'] = ''
    Data['Parametric EWMA'] = ''
   
   
    # NewData = Data[50:].reset_index().drop(['index'], axis = 1)
    NewData = Data[Period_Interval:]
    for count, i in enumerate(NewData.index):
        df = Data[count :count + Period_Interval ][Data.columns[0]]
        df = df.sort_index(ascending=False)
        NewData.loc[i, 'Historical VaR'] = VaRCalculation(df, Formula = 'Historical simulation', Period_Interval=Period_Interval)
        NewData.loc[i, 'Parametric VaR'] = VaRCalculation(df, Formula = 'Parametric Normal', Period_Interval=Period_Interval)
        NewData.loc[i, 'Parametric EWMA'] = VaRCalculation(df, Formula = 'Parametric EWMA', Period_Interval=Period_Interval)
        
    # return NewData[[Data.columns[0], 'Historical VaR', 'Parametric VaR', 'Parametric EWMA']]
    final = pd.DataFrame(NewData[['Parametric EWMA', 'Historical VaR', 'Parametric VaR', 'close_pc']])
    # final.columns = Data.columns[0]
    # final = final.rename(columns = {'Parametric EWMA' : Data.columns[0]})
    
    return final

def MarginVaR(Ticker, Portfolio, Shares):
    """
    inputs:
        ticker: ticker of the share to be analysed
        Portfolio: dataframe of shares return rates
    output:
        margVaR: marginalVaR of ticker of analysis
    """
    
    i = (Portfolio[Ticker])
    data_return = np.matmul(Portfolio, Shares)
    corr = i.corr(data_return)
    std_i = i.std()
    std_p = data_return.std()
    margVaR = corr *std_i/std_p
    
    return margVaR 

def ComponentVaR(margVar: list[str]
                 , shares: list[float]
                 , VaR_amount: float):
    
    comp_perc = [(x, y) for x in margVar for y in shares]
    comp_perc = [x*y for x,y in zip(margVar, shares)]
    
    comp_var = [x*VaR_amount for x in comp_perc]
    
    return comp_var

