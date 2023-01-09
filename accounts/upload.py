# -*- coding: utf-8 -*-
"""
Created on Fri Dec 16 12:58:08 2022

@author: bidzh
"""

from dbupload.config import *
import pandas as pd
import os

os.chdir(r'O:\VaR Startup\alpaca')

excel = ['cryptostatus', 'accountstatus', 'documenttype', 'agreements', 'contexttype', 'employmentstatus'
         , 'visatype', 'fundingsource', 'taxidtype', 'accounttype', 'enums']

database = ['cat_cryptostatus', 'cat_accountstatus', 'cat_documenttype', 'cat_agreements',
            'cat_contexttype', 'cat_employmentstatus', 'cat_visatype', 'cat_fundingsource',
            'cat_taxidtype', 'cat_accounttype', 'cat_enums']

data = {}



for i in excel:
    data[i] = pd.read_excel('categories.xlsx', sheet_name=i)
    
    
for count, i  in enumerate(data.keys()):
    temp = data[i]
    temp.to_sql(database[count], schema = 'users', if_exists='append', index = False, con = postg_engine)
    print(i+ ' is uploaded')
    

for table in database:
    sql = r'delete from {}'.format(table)
    cur.execute(sql)
    cur.commit()
    print(table)