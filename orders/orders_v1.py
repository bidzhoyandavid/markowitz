# -*- coding: utf-8 -*-
"""
Created on Mon Dec 19 15:44:08 2022

@author: bidzh
"""

from dbupload.config import *
from alpaca.broker.client import BrokerClient
from alpaca.broker.requests import MarketOrderRequest, LimitOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce

broker_client = BrokerClient(alpacaSandbox.key, alpacaSandbox.secret_key)

account = '02d1a647-f4ce-45c0-b4db-f63c36af7db5'

# =============================================================================
# classes
# =============================================================================

class MarketOrder:
    def __init__(self, account_id, symbol, qty, side, time_in_force, comission = alpacaSandbox.comission/100):
        self.account_id = account_id
        self.symbol = symbol
        self.qty = qty
        self.side = side
        self.time_in_force = time_in_force
        self.comission = comission
        
    def Execute(self):
        market_order_data = MarketOrderRequest(
                            symbol = self.symbol
                            , qty = self.qty
                            , side = self.side
                            , time_in_force = self.time_in_force
                            , comission = self.comission
            )
        
        market_order = broker_client.submit_order_for_account(
                account_id = self.account_id,
                order_data = market_order_data
                )
        
        return market_order 

     
a = MarketOrder(account, 'AAPL', 1, OrderSide.BUY, TimeInForce.GTC)

a.Execute()


# =============================================================================
# functions
# =============================================================================

def MarketOrder(account
                , symbol
                , qty
                , side
                , time_in_force
                , comission = alpacaSandbox.comission):
    
    
    market_order_data = MarketOrderRequest(
                        symbol = symbol,
                        qty = qty,
                        side = side,
                        time_in_force = time_in_force,
                        )
    
    market_order = broker_client.submit_order_for_account(
                    account_id=account,
                    order_data=market_order_data
                    )
    
    return market_order


MarketOrder(account_id, 'TSLA', 10, OrderSide.BUY, TimeInForce.GTC)


def LimitOrder(
            account
            , symbol
            , limit_price
            , qty
            , side
            , time_in_force
            , comission = 0
        ):
    
    limit_order_data = LimitOrderRequest(
                        symbol = symbol,
                        limit_price = limit_price,
                        qty = qty,
                        side = side,
                        time_in_force = time_in_force,
                        )
    
    limit_order = broker_client.submit_order_for_account(
                    account_id=account,
                    order_data=limit_order_data
                   )
    return limit_order


LimitOrder(account_id, 'TSLA', 300, 10, OrderSide.BUY, TimeInForce.FOK)
        