# -*- coding: utf-8 -*-
"""
Created on Sat Dec 24 13:41:28 2022

@author: bidzh
"""

from dbupload.config import *


from alpaca.data.historical.stock import StockHistoricalDataClient
from alpaca.data.timeframe import TimeFrame
from alpaca.data.enums import Adjustment, DataFeed
from alpaca.data.requests import StockBarsRequest, StockQuotesRequest, StockQuotesRequest
from typing import Optional, Union
from uuid import UUID
import pandas as pd
import time


stock_client = StockHistoricalDataClient(api_key = alpacaMarket.API_KEY
                                         , secret_key= alpacaMarket.SECRET_KEY)


def getStockBars(symbol_or_symbols: Union[str, list[str]]                 
                 , timeframe: TimeFrame = TimeFrame.Day
                 , start: Optional[Union[pd.to_datetime, str]] = None
                 , end: Optional[Union[pd.to_datetime, str]] = None
                 , limit: int = None
                 , adjustment: Adjustment = None
                 , feed: DataFeed = None):
    
    request = StockBarsRequest(symbol_or_symbols = symbol_or_symbols
                               , timeframe = timeframe
                               , start = start
                               , end = end
                               , limit = limit
                               , adjustment = adjustment
                               , feed = feed)
    
    data = stock_client.get_stock_bars(request)
    data = data.df.reset_index()
    
    final = pd.DataFrame()
    final = pd.concat([final, data[data['symbol'] == symbol_or_symbols[0]]], axis = 1)
    final = final[['timestamp', 'close']]
    final.columns = ['date', symbol_or_symbols[0]]
    
    if len(symbol_or_symbols) != 1:  
        for item in range(1, len(symbol_or_symbols)):
            temp = data[data['symbol'] == symbol_or_symbols[item]]
            temp = temp[['timestamp', 'close']]
            temp.columns  = ['date', symbol_or_symbols[item]]
            final = pd.merge(final, temp, how ='inner', left_on = 'date', right_on='date')    
    
    return final




# start_time = time.time()
# data = getStockBars(['AAPL', 'MSFT', 'AMZN', 'IBM',  'ISIG']
#                     , timeframe = TimeFrame.Day
#                     , start = pd.to_datetime('2010-01-01')
#                     , end = pd.to_datetime('2022-12-20'))
# print("Total Running time = {:.3f} seconds".format(time.time() - start_time))

  

def getStockQoutes(symbol_or_symbols: Union[str, list[str]]
                   , start: Optional[Union[pd.to_datetime, str]] = None
                   , end: Optional[Union[pd.to_datetime, str]] = None
                   , limit: int = None
                   , feed: DataFeed = None):
    
    request = StockQuotesRequest(symbol_or_symbols = symbol_or_symbols
                                 , start = start
                                 , end = end
                                 , feed = feed)
    
    data = stock_client.get_stock_quotes(request)
    
    return data



def getStockTradeRequest(symbol_or_symbols: Union[str, list[str]]
                         , start: Optional[Union[pd.to_datetime, str]] = None
                         , end: Optional[Union[pd.to_datetime, str]] = None
                         , limit: int = None
                         , feed: DataFeed = None):
    
    request = StockQuotesRequest(symbol_or_symbols = symbol_or_symbols
                                 , start = start
                                 , end = end
                                 , limit = limit
                                 , feed = feed)
    
    data = stock_client.get_stock_quotes(request)
    
    return data

