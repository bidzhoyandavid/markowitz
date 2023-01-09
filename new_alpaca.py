# -*- coding: utf-8 -*-
"""
Created on Thu Dec 22 11:02:48 2022

@author: bidzh
"""
import json
from dbupload.config import *
import alpaca_trade_api as atp

BASE_URL = alpacaMarket.BASE_URL
API_KEY = alpacaMarket.API_KEY
SECRET_KEY = alpacaMarket.SECRET_KEY


api = atp.REST(API_KEY, SECRET_KEY, BASE_URL)

assets = api.list_assets()


import inspect
import re

def getClassMembers(obj, name=None, mbrcat='all'):
    # name : filter by attribute name
    # mbrcat : filter members by items category : all, methods or attributes
    dic_cat= { 
        'all' : lambda a: a, 
        'meth' : lambda a: inspect.isroutine(a), 
        'attr' : lambda a:  not(inspect.isroutine(a)) 
      } 
    return [str(_name)+'  :  '+str(member)  
            for _name, member in inspect.getmembers(obj, dic_cat[mbrcat])  
            if ((name==None) or (name in _name)) and (not(re.search(r'(^\_\_|\_\_$)' ,_name))) ]

eval(getClassMembers(a)[0].split(":",1)[-1])["class"]



