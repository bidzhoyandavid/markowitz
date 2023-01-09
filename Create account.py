# -*- coding: utf-8 -*-
"""
Created on Thu Dec 15 17:47:29 2022

@author: bidzh
"""

from dbupload.config import *
from faker import Faker
import datetime as dt
from datetime import date, datetime
import pandas as pd
from random import randint
from typing import Optional



from alpaca.broker import BrokerClient
from alpaca.broker.enums import TaxIdType

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


def Acc_Agreement(
        signed_at: str = datetime.utcnow().isoformat()[:-7] + 'Z'
       
        ):
    
    agreement_data = [
        Agreement(
          agreement=AgreementType.MARGIN,
          signed_at = signed_at,
          revision = None,
          ip_address =  Faker().ipv4(),
        ),
        Agreement(
          agreement = AgreementType.ACCOUNT,
          signed_at = signed_at,
          revision = None,
          ip_address =  Faker().ipv4(),
        ),
        Agreement(
          agreement = AgreementType.CUSTOMER,
          signed_at = signed_at,
          revision = None,
          ip_address =  Faker().ipv4(),
        ),
        Agreement(
          agreement = AgreementType.CRYPTO,
          signed_at = signed_at,
          revision = None,
          ip_address =  Faker().ipv4(),
        )
    ]
    
    return agreement_data





def CreateAccount(
        # contacts
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
        , date_of_birth: str = str(date(randint(1950,2002),randint(1, 12), randint(1, 28)))
        , tax_id: str = '778-62-8144'
        , tax_id_type: str = TaxIdType.USA_SSN
        , country_of_citizenship: str = 'USA'
        , country_of_birth: str = 'USA'
        , country_of_tax_residence: str = 'USA'
        , funding_source: str = [FundingSource.EMPLOYMENT_INCOME]
        
        # disclosure
        , is_control_person: bool = False
        , is_affiliated_exchange_or_finra: bool = False
        , is_politically_exposed: bool = False
        , immediate_family_exposed: bool = False
        
        # agreement
        # , ip_address: str = Faker().ipv4()
        # , signed_at: str = "2022-09-11T18:09:33Z" # dt.datetime.utcnow().isoformat()[:-7] + 'Z'
        ):
    
    """
    The function creates account in Alpaca system and append to the database in markowitz
    """
    
    
    account_data = CreateAccountRequest(
        
                        contact = Contact(email_address = email_address
                                              , phone_number = phone_number
                                              , street_address = street_address
                                              , city = city
                                              , state = state
                                              , postal_code = postal_code
                                              , country = 'USA'
                                              ),
                        
                          
                        identity = Identity(given_name = given_name
                                            , middle_name = middle_name
                                            , family_name = family_name
                                            , date_of_birth = date_of_birth
                                            , tax_id = tax_id
                                            , tax_id_type = tax_id_type
                                            , country_of_citizenship = country_of_citizenship
                                            , country_of_birth = country_of_birth
                                            , country_of_tax_residence = country_of_tax_residence
                                            , funding_source = funding_source),
                                                
                        
                        disclosures = Disclosures(
                                                 is_control_person = is_control_person
                                               , is_affiliated_exchange_or_finra = is_affiliated_exchange_or_finra
                                               , is_politically_exposed = is_politically_exposed
                                               , immediate_family_exposed = immediate_family_exposed
                                               ),
                        
                        
                        # agreement_data = [
                        #                         Agreement(
                        #                           agreement=AgreementType.MARGIN,
                        #                           signed_at = signed_at,
                        #                           ip_address = ip_address
                        #                         ),
                        #                         Agreement(
                        #                           agreement = AgreementType.ACCOUNT,
                        #                           signed_at = signed_at,
                        #                           ip_address = ip_address
                        #                         ),
                        #                         Agreement(
                        #                           agreement = AgreementType.CUSTOMER,
                        #                           signed_at = signed_at,
                        #                           ip_address = ip_address
                        #                         ),
                        #                         Agreement(
                        #                           agreement = AgreementType.CRYPTO,
                        #                           signed_at = signed_at,
                        #                           ip_address = ip_address
                        #                         )
                        #             ]
                        
                        agreement_data = Acc_Agreement()
                        
                        )
    
    account = broker_client.create_account(account_data)
    
    return account
        
a = CreateAccount(email_address= 'aaa@bbb.com'
                  , phone_number = "555-666-7788"
                  , street_address = [Faker().address()]
                  , city = Faker().city()
                  , state = 'AL'
                  , postal_code = Faker().postcode()
                  , given_name = Faker().first_name()
                  , family_name = Faker().last_name()) 
        
    
    
        

        
        
a.account_number
a.agreements[0].agreement
a.contact.postal_code
        
account_data = CreateAccountRequest(
                    contact = Acc_Contact(email_address = "test5@test1.ru"
                                          , phone_number = "555-666-7788"
                                          , street_address = [Faker().address()]
                                          , city = Faker().city()
                                          , state = 'AL'
                                          , postal_code = Faker().postcode()),
                    
                      
                    identity = Acc_Identity(Faker().first_name()
                                            , Faker().first_name()
                                            , Faker().last_name()
                                            , "1971-01-01"),
                                            
                    
                    disclosures = Acc_DisclosureData(),
                    agreements = Acc_Agreement()
                    )
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
