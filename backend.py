# -*- coding: utf-8 -*-
"""
Created on Fri Dec 23 12:50:42 2022

@author: bidzh
"""

from dbupload.config import *
from typing import Optional, Union
from alpaca.broker import BrokerClient
from uuid import UUID, uuid1
from alpaca.broker.models.funding import (Bank, Transfer)


from alpaca.broker.enums import (BankAccountType
                                 , ACHRelationshipStatus
                                 , IdentifierType
                                 , BankStatus
                                 , TransferDirection
                                 , TransferTiming
                                 , FeePaymentMethod
                                 , TransferType
                                 , TransferStatus
                                 , TransferDirection
                                 , TransferTiming
                                 , FeePaymentMethod
                                 , TransferDirection
                                 , BankAccountType)

from alpaca.broker.requests import( 
                                    CreateAccountRequest
                                   , UpdatableContact
                                   , GetAccountActivitiesRequest
                                   , Sort
                                   , List
                                   , ActivityType
                                   , CreateACHRelationshipRequest
                                   , CreateBankRequest
                                   , CreateACHTransferRequest
                                   , CreateBankTransferRequest
                                   , GetTransfersRequest
                                   )
from alpaca.trading.enums import (OrderType
                                  , OrderSide
                                  , OrderClass
                                  , TimeInForce
                                  , OrderStatus
                                  , AssetExchange
                                  , AssetClass
                                  , AssetStatus
                                  )

from alpaca.trading.requests import (TakeProfitRequest
                                     , StopLossRequest
                                     , GetOrdersRequest
                                     , ReplaceOrderRequest
                                     , CancelOrderResponse
                                     , GetAssetsRequest
                                     , GetPortfolioHistoryRequest
                                     , CreateWatchlistRequest
                                     , UpdateWatchlistRequest)

from alpaca.trading.models import Position, ClosePositionResponse, Order
from alpaca.broker.requests import OrderRequest


BROKER_API_KEY = alpacaSandbox.key
BROKER_SECRET_KEY = alpacaSandbox.secret_key
BROKER_URL = alpacaSandbox.url

broker_client = BrokerClient(
                    api_key=BROKER_API_KEY,
                    secret_key=BROKER_SECRET_KEY,
                    sandbox=True,
                )

# =============================================================================
# Account part
# =============================================================================


def getAccountByID(accountID: Union[UUID, str]):
    
    account = broker_client.get_account_by_id(accountID)
        
    return account

# a = getAccountByID('9eda3cd0-f3a0-4ad3-98fd-0d831eff3236')


def deleteAccountByID(accountID: Union[UUID, str]):
    delete = broker_client.delete_account(accountID)
    
    return delete
    

# =============================================================================
# Trade part
# =============================================================================
  

def getTradeAccountByID(accountID: Union[UUID, str]):
    info = broker_client.get_trade_account_by_id(accountID)
    
    return info

# a = getTradeAccountByID('9a2c67d4-d33d-4b0f-b6d4-9949039ca873')
# a.__dict__    



def getTradeConfigAccountByID(accountID: Union[UUID, str]):
    trade = broker_client.get_trade_configuration_for_account(accountID)
    
    return  trade

# a = getTradeConfigAccountByID('9a2c67d4-d33d-4b0f-b6d4-9949039ca873')


def getAccountActivities(account_id: Union[UUID, str] 
                        , activity_types: List[ActivityType] = None
                        , date: pd.to_datetime = None
                        , until: pd.to_datetime = None
                        , after: pd.to_datetime = None
                        , direction: Sort = None
                        , page_size: int = None
                        , page_token: Optional[Union[UUID, str]] = None) :   
    
    activity_filter = GetAccountActivitiesRequest(account_id = account_id
                                                  , activity_types  = activity_types
                                                  , date = date
                                                  , until = until
                                                  , after = after
                                                  , direction = direction
                                                  , page_size = page_size
                                                  , page_token = page_token)
    data = broker_client.get_account_activities(activity_filter = activity_filter)
    
    return data
        

# getAccountActivities('9a2c67d4-d33d-4b0f-b6d4-9949039ca873', direction = Sort.DESC)


# =============================================================================
# Orders part
# =============================================================================

def submitOrder(accountID: Union[UUID, str]
                , symbol: str
                , side: OrderSide
                , type_order: OrderType
                , time_in_force: TimeInForce
                , qty: float = None
                , notional: float = None
                , order_class: OrderClass = None
                , extended_hours: bool = None
                , client_order_id: str = None
                , take_profit: TakeProfitRequest = None
                , stop_loss: StopLossRequest = None
                , commission: float = alpacaSandbox.comission):
    
    order = OrderRequest(symbol = symbol
                         , side = side
                         , type = type_order
                         , time_in_force = time_in_force
                         , qty = qty
                         , notional = notional
                         , order_class = order_class
                         , extended_hours = extended_hours
                         , client_order_id = client_order_id
                         , take_profit = take_profit
                         , stop_loss = stop_loss
                         , commission = commission)
    submit = broker_client.submit_order_for_account(accountID, order)
    
    return submit
    
    
# a = submitOrder('9a2c67d4-d33d-4b0f-b6d4-9949039ca873'
#                 , 'IBM'
#                 , OrderSide.BUY
#                 , OrderType.MARKET
#                 , TimeInForce.DAY
#                 , qty = 100)
    
    
def getAllOrderByAccountID(accountID: Union[UUID, str]
                           , status: OrderStatus = None
                           , limit: int = None
                           , after: pd.to_datetime = None
                           , until: pd.to_datetime = None
                           , direction: Sort = None
                           , nested: bool = None
                           , side: OrderSide = None
                           , symbols: list[str] = None):
    
    orderRequest = GetOrdersRequest(status = status
                                    , limit = limit
                                    , after = after
                                    , until = until
                                    , direction = direction
                                    , nested = nested
                                    , side = side
                                    , symbols = symbols)
    
    data = broker_client.get_orders_for_account(accountID, orderRequest)
    
    return data
    

def replaceOrderByID(accountID: Union[UUID, str]
                     , order_id: Union[UUID, str]
                     , qty: int = None
                     , time_in_force: TimeInForce = None
                     , limit_price: float = None
                     , stop_price: float = None
                     , trail: float = None
                     , client_order_id: str = None):
    
    replace = ReplaceOrderRequest(qty = qty
                                  , time_in_force = time_in_force
                                  , limit_price = limit_price
                                  , stop_price = stop_price
                                  , trail = trail
                                  , client_order_id = client_order_id)
    
    replOrder = broker_client.replace_order_for_account_by_id(accountID
                                                , order_id
                                                , replace)
    
    return replOrder

def cancelALLOrders(accountID: Union[UUID, str]):
    txt = broker_client.CancelOrderResponse(accountID, 505)
    
    return txt

def cancelOrderByqID(accountID: Union[UUID, str], orderID: Union[UUID, str]):
    
    broker_client.cancel_order_for_account_by_id(accountID, orderID)
    
    return 'The order of {} is canceled'.format(orderID)
    
# =============================================================================
# Positions part
# =============================================================================

def getAllPositionsByAccountID(accountID: Union[UUID, str]):
    
    data = broker_client.get_all_positions_for_account(accountID)
    
    return data

# getALLPositionsByAccountID('9a2c67d4-d33d-4b0f-b6d4-9949039ca873')


def getOpenPositionByAccountID(accountID: Union[UUID, str]
                               , assetID: Union[UUID, str]):
    
    data = broker_client.get_open_position_for_account(accountID, assetID)
    
    return data

def closeAllPositions(accountID: Union[UUID, str]
                      , cancel_orders: bool) -> list[ClosePositionResponse]:
    data = broker_client.close_all_positions_for_account(accountID, cancel_orders)
    
    return data
    
    
def closePositionByAccountID(accountID: Union[UUID, str]
                             , asssetID: Union[UUID, str]
                             , status: AssetStatus = None
                             , asset_class: AssetClass = None
                             , exchange: AssetExchange = None):
    
    request = GetAssetsRequest(status = status
                               , asset_class = asset_class
                               , exchange = exchange)
    
    order = broker_client.close_position_for_account(accountID
                                                     , asssetID
                                                     , request)
    
    return order
        



def getPortfolioHistoryByID(accountID: Union[UUID, str]                            
                            , period: str = None
                            , timeframe: str = None
                            , date_end: pd.to_datetime = None
                            , extended_hours: bool = None):
    
    historyRequest = GetPortfolioHistoryRequest(period = period
                                                , timeframe = timeframe
                                                , date_end = date_end
                                                , extended_hours = extended_hours)
    
    data = broker_client.get_portfolio_history_for_account(accountID, historyRequest)
    
    return data
    

# =============================================================================
# watchlist
# =============================================================================

def CreateWatchList(accountID: Union[UUID, str]
                    , name: str
                    , symbols: list[str]):
    
    request = CreateWatchlistRequest(name = name
                                     , symbols = symbols)
    
    data = broker_client.create_watchlist_for_account(
            accountID
            , request
        )
    
    return data


def getWatchList(accountID):
    
    data = broker_client.get_watchlists_for_account(accountID)
    
    return data



def getWatchListAccountByID(accountID: Union[UUID, str]
                            , watchlistID: Union[UUID, str]):
    
    data = broker_client.get_watchlist_for_account_by_id(accountID, watchlistID)
    
    return data


def updateWatchListByID(accountID: Union[UUID, str]
                        , watchlistID: Union[UUID, str]
                        , name: str = None
                        , symbols: List[str] = None):
    
    request = UpdateWatchlistRequest(name = name, symbols = symbols)
    
    data = broker_client.update_watchlist_for_account_by_id
    
    return data
    
 
def deleteWatchListByID(accountID: Union[UUID, str]
                        , watchlistID: Union[UUID, str]):
    
    broker_client.delete_watchlist_from_account_by_id(accountID, watchlistID)
    
    return "The watchlist {} is deleted".format(watchlistID)
    
    
    
def addAssetsToWatchlist(accountID: Union[UUID, str]
                        , watchlistID: Union[UUID, str]):
    
    data = add_asset_to_watchlist_for_account_by_id(accountID, watchlistID)
    
    return data

def removeAssetFromWatchlist(accountID: Union[UUID, str]
                             , watchlistID: Union[UUID, str]
                             , symbol: str):
    
    data = broker_client.remove_asset_from_watchlist_for_account_by_id(accountID
                                                                       , watchlistID
                                                                       , symbol)
    
    return data
      


# =============================================================================
# ACH Relationship
# =============================================================================

def createACHRelation(accountID: Union[UUID, str]
                      , account_owner_name: str
                      , bank_account_type: BankAccountType
                      , bank_account_number: str
                      , bank_routing_number: str):
    
    request = CreateACHRelationshipRequest(
                    account_owner_name = account_owner_name,
                    bank_account_type = bank_account_type,
                    bank_account_number = bank_account_number,
                    bank_routing_number = bank_routing_number,
                )

    ach = broker_client.create_ach_relationship_for_account(accountID, request)
    
    return ach

def getACHRelationship(accountID: Union[UUID, str]
                       , statuses: Optional[list[ACHRelationshipStatus]] = None):

    data = broker_client.get_ach_relationships_for_account(account_id = accountID
                                                           , statuses = statuses)
    
    return data

def deleteACHRelationship(accountID: Union[UUID, str]
                          , achRelationshipID:  Union[UUID, str]):
    
    return broker_client.delete_ach_relationship_for_account(accountID, achRelationshipID)


# =============================================================================
# Bank relatioship
# =============================================================================


def createBankForAccount(accountID: Union[UUID, str]
                         , name: str
                         , bank_code_type: IdentifierType
                         , bank_code: str
                         , account_number: str
                         , country: str = None
                         , state_province: str = None
                         , postal_code: str = None
                         , city: str = None
                         , street_address: str = None):
    
    request = CreateBankRequest(name = name
                                , bank_code_type = bank_code_type
                                , bank_code = bank_code
                                , account_number = account_number
                                , country = country
                                , state_province = state_province
                                , postal_code = postal_code
                                , city = city
                                , street_address = street_address)
    
    create = broker_client.create_bank_for_account(accountID
                                                   , request)
    
    return create

def getBanksForAccount(accountID: Union[UUID, str]):
    
    return broker_client.get_banks_for_account(accountID)


def deleteBankForAccount(accountID: Union[UUID, str]
                         , bankID: Union[UUID, str]):
    return broker_client.delete_bank_for_account(accountID, bankID)



# =============================================================================
# Create Transfer
# =============================================================================

def createTransferForAccount(accountID: Union[UUID, str]
                             , typeTransfer: Union['ach', 'bank']
                             , amount: str
                             , direction: TransferDirection
                             , timing: TransferTiming                             
                             , relationship_id: Optional[UUID]
                             , bankID: Optional[UUID]                          
                             , fee_payment_method: FeePaymentMethod = None
                             , additional_information: str = None):
    
    if typeTransfer == 'ach':
         request = CreateACHTransferRequest(amount = amount
                                            , direction = direction
                                            , timing = timing
                                            , fee_payment_method = fee_payment_method
                                            , relationship_id = relationship_id
                                            , transfer_type = TransferType.ACH)
    else:
        request = CreateBankTransferRequest(amount = amount
                                            , direction = direction
                                            , timing = timing
                                            , fee_payment_method = fee_payment_method
                                            , bank_id = bankID
                                            , transfer_type = TransferType.WIRE)
        
    transfer = broker_client.create_transfer_for_account(accountID, request)
    
    return transfer
         

def getTransferForAccount(accountID: Union[UUID, str]
                          , transfers_filter: Optional[GetTransfersRequest] = None
                          , max_items_limit: Optional[int] = None
                          , handle_pagination = None
                          , direction: TransferDirection = None
                          , limit: int = None, offset: int = None):

    request = GetTransfersRequest(direction = direction
                                  , limit = limit
                                  , offset = offset)
    
    data = broker_client.get_transfers_for_account(account_id = accountID
                                                   , transfers_filter = request
                                                   , max_items_limit = max_items_limit
                                                   , handle_pagination = handle_pagination)
    
    return data

def cancelTransferForAccount(accountID: Union[UUID, str]
                             , transferID: Union[UUID, str]):
    
    return broker_client.cancel_transfer_for_account(accountID, transferID)




