# -*- coding: utf-8 -*-
"""
Created on Mon Dec 19 16:43:38 2022

@author: bidzh
"""

from alpaca.broker import BrokerClient
from dbupload.config import *

broker_client = BrokerClient(alpacaSandbox.key, alpacaSandbox.secret_key)

# account to get positions for
account = '02d1a647-f4ce-45c0-b4db-f63c36af7db5'

positions = broker_client.get_all_positions_for_account(account_id=account)
 