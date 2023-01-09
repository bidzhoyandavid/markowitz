# -*- coding: utf-8 -*-
"""
Created on Tue Dec 20 15:42:36 2022

@author: bidzh
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Dec 15 17:47:29 2022

@author: bidzh
"""

from dbupload.config import *
from faker import Faker
from datetime import date, datetime
import pandas as pd
from typing import Optional
from random import randint


from alpaca.broker import BrokerClient

BROKER_API_KEY = alpacaSandbox.key
BROKER_SECRET_KEY = alpacaSandbox.secret_key
BROKER_URL = alpacaSandbox.url

broker_client = BrokerClient(
                    api_key=BROKER_API_KEY,
                    secret_key=BROKER_SECRET_KEY,
                    sandbox=True,
                )

# =============================================================================
# create an account
# =============================================================================

from alpaca.broker.client import BrokerClient
from alpaca.broker.models import (
                        Contact,
                        Identity,
                        Disclosures,
                        Agreement
                    )
from alpaca.broker.requests import CreateAccountRequest
from alpaca.broker.enums import TaxIdType, FundingSource, AgreementType


def getIDAgreement(agreem):
        
    id_agreement = pd.read_sql('select id_record from users.cat_agreements where attribute_name = %(agr)s'
                               , params ={'agr': agreem}
                               , con = post_conn)   
    if id_agreement.empty:        
        return False
    else:
        return  True
    
        

def getIDTaxIDType(tax_type):
    
    tax_id_type = pd.read_sql('select id_record from users.cat_taxidtype where attribute_name = %(agr)s'
                              , params = {'agr': tax_type}
                              , con = post_conn)
    
    if tax_id_type.empty:
        raise ValueError('There is no {} tax_id type'.format(tax_type))
    else:
        return tax_id_type['id_record'].values[0]  
          
def getIDFundingSource(source):
    
    id_source = pd.read_sql('select id_record from users.cat_fundingsource where attribute_name = %(id)s'
                            , params = {'id': source.lower()}
                            , con = post_conn)
    if id_source.empty:
        raise ValueError('There is no {} funding source'.format(source))
    
    return id_source['id_record'].values[0]

def getIDAccountStatus(statusName):
    
    id_status = pd.read_sql('select id_record from users.cat_accountstatus where attribute_name = %(id)s'
                            , params = {'id': statusName}
                            , con = post_conn)
    if id_status.empty:
        raise ValueError('There is no {} status'.format(statusName))
    
    return id_status['id_record'].values[0]


def Acc_Contact(email_address
                , phone_number
                , street_address
                , city
                , state
                , postal_code
                , country = "USA"):
    
    contact_data = Contact(
        email_address = email_address
        , phone_number = phone_number
        , street_address = street_address
        , city = city
        , state = state
        , postal_code = postal_code
        , country = country
        )
    
    return contact_data
        
def Acc_Identity(given_name
                 , middle_name
                 , family_name
                 , date_of_birth
                 , tax_id = '778-12-8144'
                 , tax_id_type = TaxIdType.USA_SSN
                 , country_of_citizenship = "USA"
                 , country_of_birth = "USA"
                 , country_of_tax_residence = "USA"
                 , funding_source = [FundingSource.EMPLOYMENT_INCOME]
                 ):
    
    identity_data = Identity(
        given_name = given_name,
        middle_name = middle_name,
        family_name = family_name,
        date_of_birth = date_of_birth,
        tax_id = tax_id,
        tax_id_type = tax_id_type,
        country_of_citizenship = country_of_citizenship,
        country_of_birth = country_of_birth,
        country_of_tax_residence = country_of_tax_residence,
        funding_source = funding_source
        )
    return identity_data

def Acc_DisclosureData(is_control_person = False
                       , is_affiliated_exchange_or_finra = False
                       , is_politically_exposed = False
                       , immediate_family_exposed = False):
    disclosure_data = Disclosures(
        is_control_person = is_control_person,
        is_affiliated_exchange_or_finra = is_affiliated_exchange_or_finra,
        is_politically_exposed = is_politically_exposed,
        immediate_family_exposed = immediate_family_exposed,
        )
    return disclosure_data

def Acc_Agreement(
        signed_at: str = datetime.utcnow().isoformat()[:-7] + 'Z'
        , ip_address = Faker().ipv4()
        ):
    
    agreement_data = [
        Agreement(
          agreement=AgreementType.MARGIN,
          signed_at = signed_at,
          revision = None,
          ip_address =  ip_address,
        ),
        Agreement(
          agreement = AgreementType.ACCOUNT,
          signed_at = signed_at,
          revision = None,
          ip_address =  ip_address,
        ),
        Agreement(
          agreement = AgreementType.CUSTOMER,
          signed_at = signed_at,
          revision = None,
          ip_address =  ip_address,
        ),
        Agreement(
          agreement = AgreementType.CRYPTO,
          signed_at = signed_at,
          revision = None,
          ip_address = ip_address,
        )
    ]
    
    return agreement_data



def CreateAccount(
        email_address: str
      , phone_number: str
      , street_address: str
      , city: str
      , state: str
      , postal_code: str
      
      # identity
      , given_name: str
      , family_name: str
      , middle_name: Optional[str] = None  
      , date_of_birth = str(date(randint(1950,2002),randint(1, 12), randint(1, 28)))
        ):
    account_data = CreateAccountRequest(
                        contact = Acc_Contact(email_address = email_address
                                              , phone_number = phone_number
                                              , street_address = street_address
                                              , city = city
                                              , state = state
                                              , postal_code = postal_code),
                        
                          
                        identity = Acc_Identity( given_name = given_name
                                                , middle_name = middle_name
                                                , family_name = family_name
                                                , date_of_birth = date_of_birth),
                                                
                        
                        disclosures = Acc_DisclosureData(),
                        agreements = Acc_Agreement()
                        )
    account = broker_client.create_account(account_data)
    
    # data = pd.DataFrame(index = [0])
    
    # # general info
    # data['account_number'] = account.account_number
    # data['id_account'] = account.id
    # data['created_at'] = account.created_at  
    # data['status'] = getIDAccountStatus(account.status.name)
    
    # # contact info
    # data['email_address'] = account.contact.email_address
    # data['phone_number'] = account.contact.phone_number
    # # date['city'] = account.contact.city
    # data['state'] = account.contact.state
    # data['street_address'] = account.contact.street_address
    # data['postal_code'] = account.contact.postal_code
    
    # # identity info
    # data['given_name'] = account.identity.given_name
    # data['middle_name'] = account.identity.middle_name
    # data['family_name'] = account.identity.family_name
    # data['date_of_birth'] = account.identity.date_of_birth
    # data['tax_id'] = account.identity.tax_id
    # data['tax_id_type'] = getIDTaxIDType(account.identity.tax_id_type.name)
    # data['country_of_birth'] = account.identity.country_of_birth
    # data['country_of_citizenship'] = account.identity.country_of_citizenship
    # data['country_of_tax_residence'] = account.identity.country_of_tax_residence
    # data['funding_source'] = getIDFundingSource(account.identity.funding_source[0].name)
    
    # # disclosure
    # data['is_affiliated_exchange_or_finra'] = account.disclosures.is_affiliated_exchange_or_finra
    # data['is_control_person'] = account.disclosures.is_control_person
    # data['is_politically_exposed'] = account.disclosures.is_politically_exposed
    # data['immediate_family_exposed'] = account.disclosures.immediate_family_exposed
     
    
    # # agreement 
    # data['margin_agreement'] = getIDAgreement(account.agreements[0].agreement.name)
    # data['account_agreement'] = getIDAgreement(account.agreements[1].agreement.name)
    # data['customer_agreement'] = getIDAgreement(account.agreements[2].agreement.name)
    # data['signed_at'] = account.agreements[0].signed_at
    # data['ip_address'] = account.agreements[0].ip_address
    
    # data.columns = ['account_number', 'id_account',  'created_at', 'id_status', 'email', 
    #                 'phone','state', 'street_address',  'postal_code', 'given_name', 'middle_name', 
    #                 'family_name', 'date_of_birth', 'tax_id', 'tax_id_type', 'county_of_birth',
    #                 'country_of_citizen', 'county_of_tax_residence', 'id_funding_source', 'is_affiliated_exchange_or_finra', 
    #                 'is_control_person', 'is_politically_exposed', 'immediate_family_exposed', 
    #                 'margin', 'account', 'customer', 'signed_at', 'ip_address']

    
    # insert = data.to_sql( 'fct_users',  schema = 'users', if_exists='append', con = postg_engine, index = False)        
    
    return  account #"Account is created"
    
  
        
a = CreateAccount(email_address='dav30@davo.com'
              , phone_number = '888-999-1111'
              , street_address = [Faker().address()]
              , city = Faker().city()
              , state = 'AL'
              , postal_code = Faker().postcode()
              , given_name=Faker().first_name()
              , family_name= Faker().last_name())


