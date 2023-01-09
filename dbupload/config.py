# -*- coding: utf-8 -*-
"""
Created on Wed Dec 14 12:00:25 2022

@author: bidzh
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import psycopg2
import pandas as pd

post_conn = psycopg2.connect(
    host="localhost",
    database="markowitz",
    user="postgres",
    password="sql")
cur = post_conn.cursor()  


postg_engine = create_engine('postgresql+psycopg2://postgres:sql@localhost:5432/markowitz')

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=postg_engine)

def getDB():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class constant:
    url = 'https://www.alphavantage.co/query'
    api_key = 'IHGO514P7E4X0K30'


class alpacaSandbox:
    url = 'https://broker-api.sandbox.alpaca.markets'
    key = 'CKVW5TK1MK7HW519I859'
    secret_key = 'l2P59bVmDT3cA1UgC4PQ3jAygMVLmsxtTrABkmEZ'
    comission = 1.05
    
    
class alpacaMarket:
    BASE_URL = 'https://api.alpaca.markets'
    API_KEY = 'AKZ9PIBL6Q7SWI36HIFV'
    SECRET_KEY = 'K8iymgFAnng7beaA9A3E5OvLyef3FT8004v1j54d'
