# -*- coding: utf-8 -*-
"""
Created on Wed Dec 14 13:34:49 2022

@author: bidzh
"""

# =============================================================================
# configuration and libraries
# =============================================================================
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
import os
from pathlib import Path
import pandas as pd
import time
import requests as re
import numpy as np
import csv
import psycopg2
from datetime import datetime, timedelta
from sqlalchemy import create_engine




from dbupload.config import *

url = constant.url
api_key = constant.api_key


# =============================================================================
# Listing part
# =============================================================================

from dbupload.listing import *

all_data = pd.DataFrame()
exchange_list = ['NASDAQ', 'NYSE', 'AMEX']


for exchange in exchange_list:
    PATH = "D:\VaR Startup\chromedriver.exe" # change path once move to cloud
    driver = webdriver.Chrome(PATH)
    
    # download the listed companies of selected exchange
    driver.get("https://www.nasdaq.com/market-activity/stocks/screener?exchange={}".format(exchange))
    driver.implicitly_wait(5)
    
    link = driver.find_element(By.CLASS_NAME, "nasdaq-screener__download")
    link.click()
    
    time.sleep(20)
    # read data
    folder = r"C:\Users\bidzh\Downloads"
    result = sorted(Path(folder).glob("*.csv"))  
    print(len(result))
    
    data = pd.read_csv(result[0], header = 0, sep = ',')
    data['Exchange'] = exchange
    
    all_data = pd.concat([all_data, data], axis = 0)
    
    # delete from directore
    os.remove(result[0])

all_data = all_data.replace(np.nan, 'Not defined')
all_data['IPO Year'] = all_data['IPO Year'].replace('Not defined', np.nan)

all_data_final = all_data[['Symbol', 'Name', 'Country', 'IPO Year', 'Sector', 'Industry', 'Exchange']]
all_data_final['Status'] = 'Active'

# --------------------------- detect new countries, sectors, industries -------------------
WebCounrty = pd.DataFrame(all_data['Country'].unique())
WebCounrty.columns = ['country_name']

WebSectors = pd.DataFrame(all_data['Sector'].unique())
WebSectors.columns = ['sector_name']

Webindustry = pd.DataFrame(all_data['Industry'].unique())
Webindustry.columns = ['indusrty_name']

DetectNewCountry(WebCounrty)
DetectNewSector(WebSectors)
DetectNewIndustry(Webindustry)

# --------------------------- update tables ------------------------------------ 
DBcountries  = pd.read_sql("select * from trade_data.cat_countries", con = postg_engine)
DBsectors    = pd.read_sql("select * from trade_data.cat_sectors",   con = postg_engine)
DBindustry   = pd.read_sql("select * from trade_data.cat_industries", con = postg_engine)

DBAll_data = pd.read_sql("select * from trade_data.cat_companies", con = postg_engine)

compare = pd.merge(DBAll_data, all_data_final, how = 'outer', left_on = 'symbol', right_on = 'Symbol', indicator=True)
compare_NewCompany = compare[compare['_merge'] == 'right_only']
compare_Delisted = compare[compare['_merge'] == 'left_only']

if len(compare_NewCompany) != 0:
    InsertNewCompany()
    
if len(compare_Delisted) != 0:
    UpdateStatusCompany(compare_Delisted)

# =============================================================================
# currency upload
# =============================================================================

from dbupload.currencyupload import *


physical = pd.read_sql('select * from trade_data.cat_physical_currencies', con = postg_engine)
physical.index = physical['currency_code']
physical = physical.drop(columns = ['id_physical', 'currency_code'])


error_curr = currUpload(physical, 'full')

# =============================================================================
# crypto upload
# =============================================================================

all_crypto = pd.read_sql('select crypto_code from trade_data.cat_crypto_currencies', con = postg_engine)
all_crypto.index = all_crypto['crypto_code']

error_crypto = cryptoUpload()




