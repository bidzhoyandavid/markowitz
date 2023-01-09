# -*- coding: utf-8 -*-
"""
Created on Wed Dec 14 13:10:48 2022

@author: bidzh
"""

import pandas as pd



def getCryptoID(crypto_code):
    
    id_crypto = pd.read_sql('select id_crypto from trade_data.cat_crypto_currencies where crypto_code = %(crypto)s',
                            params = {'crypto': crypto_code},
                            con = postg_engine)
    id_crypto = id_crypto.iloc[0,0]
    return id_crypto

def cryptoUpload():
    """
    the functions upload prices into database
    """
    
    error = []
    for crypto in all_crypto.index:
        try:
            query = {
                'function': 'DIGITAL_CURRENCY_DAILY'
                , 'symbol': crypto
                , 'market': 'USD'
                , 'apikey': API_KEY            
                }
            
            s = re.Session()
                
            response = s.get(url, params = query)
            
            if response.status_code != 200:
                raise ValueError('The status code is not 200')
            
            temp = response.json()['Time Series (Digital Currency Daily)']
            data = pd.DataFrame.from_dict(temp).T.astype(float)                
            
            sub_data = data[data.columns[data.columns.str.contains('a.')]]
            sub_data.columns   = ['price_open', 'price_high', 'price_low', 'price_close', 'market_cap']
            sub_data['date_at'] = pd.to_datetime(sub_data.index)
            sub_data['id_crypto'] = getCryptoID(crypto) 
            temp = pd.to_sql('select * from trade_data.fct_prices_crypto where id_crypto::text = %(id)s'
                             , params = {'id': getCryptoID(crypto).astype(str)}
                             , con = postg_engine).drop(columns = ['id_record'])
            
            temp['date_at'] = pd.to_datetime(temp['date_at'])
            df3 = pd.concat([data, temp]).drop_duplicates(keep = False)
            
            df3.to_sql('fct_prices_crypto', con=postg_engine, if_exists='append',  schema= 'trade_data' ,index=False)

        except:
            error.append(crypto)
    
    return error