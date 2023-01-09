# -*- coding: utf-8 -*-
"""
Created on Mon Dec 26 16:32:44 2022

@author: bidzh
"""

from backend import *


accountID = '9a2c67d4-d33d-4b0f-b6d4-9949039ca873'


accountDetails = getAccountByID(accountID)

accountDetails.__dict__


# =============================================================================
# ach rel
# =============================================================================

ach_relationship = createACHRelation(accountID = accountID
                                     , account_owner_name = '{} {}'.format(accountDetails.identity.given_name,   accountDetails.identity.family_name)                         
                                     , bank_account_type = BankAccountType.SAVINGS
                                     , bank_account_number = '123456789abc'
                                     , bank_routing_number = '121000358')


transfer = createTransferForAccount(accountID = accountID
                                    , typeTransfer = 'ach'
                                    , amount = '30000'
                                    , direction = TransferDirection.INCOMING
                                    , timing = TransferTiming.IMMEDIATE
                                    , relationship_id = getACHRelationship(accountID)[0].id # put here the relationship ID getting from getACHRelaitionship
                                    , bankID = uuid1())


# =============================================================================
# bank rel
# =============================================================================
bank_relationship = createBankForAccount(accountID = accountID
                                         , name = '{} {}'.format(accountDetails.identity.given_name,   accountDetails.identity.family_name)           
                                         , bank_code_type = IdentifierType.ABA
                                         , bank_code = '026009593'
                                         , account_number = '1234567899')

transfer_bank = createTransferForAccount(accountID = accountID
                                        , typeTransfer = 'bank'
                                        , amount = '20000'
                                        , direction = TransferDirection.INCOMING
                                        , timing = TransferTiming.IMMEDIATE
                                        , relationship_id = bank_relationship.id
                                        , bankID = uuid1())

# =============================================================================
# orders
# =============================================================================


order = submitOrder(accountID = accountID
                    , symbol = 'AAPL'
                    , side = OrderSide.BUY
                    , type_order = OrderType.MARKET
                    , time_in_force = TimeInForce.GTC
                    , qty = 10)


getOrder = getAllOrderBYAccountID(accountID = accountID)


replaceOrderBYID(accountID, getOrder[0].id, qty = 30)

cancelOrderBYID(accountID, getOrder[0].id)


# =============================================================================
# watchlist
# =============================================================================

a = CreateWatchList(accountID, 'Watchlist1', ['IBM', 'TSLA'])
a.assets[0]




getAccountActivities('9a2c67d4-d33d-4b0f-b6d4-9949039ca873', direction = Sort.DESC)


# =============================================================================
# positions
# =============================================================================


pos = getAllPositionsByAccountID(accountID)

pos[0].asset_id


trade = getTradeAccountByID(accountID)

closePositionByAccountID(accountID, pos[0].asset_id)










