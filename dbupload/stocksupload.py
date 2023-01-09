# -*- coding: utf-8 -*-
"""
Created on Wed Dec 14 12:23:39 2022

@author: bidzh
"""


def getName(name):
    if "^" in name:
       name = name.replace('^', '-P-')    
    return name

def stocksUplaod(outputsize):
    """
    The function uploads the stock prices data into database
    
    intput:
        outputsize: full - full data; compact - last 100 data
    """
    
    error = []

    for i in allStocks.index:
        id_company = allStocks.loc[i, 'id_company']
        symb = getName(allStocks.loc[i, 'symbol'])
        
        try:
            Query = {
                  'function': 'TIME_SERIES_DAILY_ADJUSTED'
                , 'symbol': symb
                , 'outputsize' : outputsize
                , 'datatype': 'json'
                , 'apikey': API_KEY
                }
            
            response = re.get(url, params = Query)
            StockDf = pd.DataFrame.from_dict(response.json()['Time Series (Daily)']).T
            StockDf = StockDf.reset_index()
            StockDf['id_company'] = id_company
            StockDf.columns = ['date_at','price_open', 'price_high', 'price_low', 'price_close'
                               , 'adj_close', 'volume', 'dividend', 'Split', 'id_company' ]
            
            StockDf = StockDf[['date_at','price_open', 'price_high', 'price_low', 'price_close', 'volume', 'id_company']]
            StockDf['date_at'] = pd.to_datetime(StockDf['date_at'])
            
            for i in ['price_open', 'price_high', 'price_low', 'price_close', 'volume']:
                StockDf[i] = pd.to_numeric(StockDf[i], errors = 'coerce')
            
            StockDf.to_sql('fct_prices_stock', con=postg_engine, if_exists='append',  schema= 'trade_data' ,index=False)
        except:
            error.append(symb)
        
        return error