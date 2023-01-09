# -*- coding: utf-8 -*-
"""
Created on Wed Dec 14 12:29:13 2022

@author: bidzh
"""

import pandas as pd
import requests as re



def getIDCurrency(cur_name):
    """
        the function returns ID_currency by the code of currency
    """
        
    id_cur = pd.read_sql('select id_physical from trade_data.cat_physical_currencies where currency_code = %(curr)s',
                        params = {'curr': cur_name}, 
                       con = postg_engine)
    id_cur = id_cur.iloc[0,0]
    return id_cur

def currUpload(curr_data, outputsize):
    
    """
        the fucntion uploads currency prices to USD into database
    input:
        curr_data: dataframe with currency codes
        outputsize: full or compact; full - the whole data; compact - last 100 points
    output:
        error: list of currencies with error of inserting
    """
    
    error = []
    for curr in curr_data.index:
        try:
            query = {
                'function': 'FX_DAILY'
                        , 'from_symbol': curr
                        , 'to_symbol': 'USD'
                        , 'outputsize': outputsize
                        , 'apikey': API_KEY 
                }
            s = re.Session()
            response = s.get(url, params = query)
        
            if response.status_code != 200:
                raise ValueError('The status code is not 200')
        
            temp = response.json()
            data = pd.DataFrame.from_dict(temp['Time Series FX (Daily)']).T
            data = data.astype(float)
        
            data = data.reset_index().rename(columns = {'index': 'date_at'})
            data.columns = ['date_at', 'price_open', 'price_high', 'price_low', 'price_close']
            data['date_at'] = pd.to_datetime(data['date_at'])
            data['id_physical'] = getIDCurrency(curr)
        
            temp = pd.read_sql('select * from trade_data.fct_prices_currency where id_physical::text = %(id)s'
                               , params = {'id': getIDCurrency(curr).astype(str)}
                               , con = postg_engine).drop(columns = ['id_record'])
        
            temp['date_at'] = pd.to_datetime(temp['date_at'])
        
        
            df3 = pd.concat([data, temp]).drop_duplicates(keep = False)
            df4 = pd.concat([df3, data]).drop_duplicates(keep=False)
                             
                             
            df4.to_sql('fct_prices_currency', con=postg_engine, if_exists='append',  schema= 'trade_data', index=False)
        except:
            error.append(curr)
