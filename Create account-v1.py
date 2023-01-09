# -*- coding: utf-8 -*-
"""
Created on Fri Dec 16 12:02:20 2022

@author: bidzh
"""


from dbupload.config import *
from faker import Faker
from datetime import datetime 
import pandas as pd


from alpaca.broker import BrokerClient
from alpaca.broker.client import BrokerClient
from alpaca.broker.models import (
                        Contact,
                        Identity,
                        Disclosures,
                        Agreement
                    )
from alpaca.broker.requests import CreateAccountRequest
from alpaca.broker.enums import TaxIdType, FundingSource, AgreementType

# =============================================================================
# authorization
# =============================================================================

BROKER_API_KEY = alpacaSandbox.key
BROKER_SECRET_KEY = alpacaSandbox.secret_key
BROKER_URL = alpacaSandbox.url

broker_client = BrokerClient(
                    api_key=BROKER_API_KEY,
                    secret_key=BROKER_SECRET_KEY,
                    sandbox=True,
                )

# =============================================================================
# helping functions
# =============================================================================

class UserExistsError(Exception):
    def __init__(self, msg):
        self.msg = msg
        
    def __repr__(self):
        return self.msg

def getIDbyEmail(email):
    """
        The functions gets email of user
    """
    
    user = pd.read_sql('select * from users.fct_user where email = %(em)s'
                       , params = {'em': email}
                       , con = postg_engine)
    
    if user.empty:
        return None
    else:
        raise UserExistsError('The user with the {} email already exists')


# =============================================================================
# class of account creating
# =============================================================================
class AccountData(CreateAccountRequest):
    def __init__(self, 
                 # Contact
                 email_address, phone_number, street_address, city, state, postal_code, country,
                 
                 # Identity 
                 given_name, middle_name, family_name, date_of_birth, tax_id, tax_id_type,
                 country_of_citizenship, country_of_birth, country_of_tax_residence, funding_source,
                 
                 # Disclosure
                 is_control_person, is_affiliated_exchange_or_finra
                 , is_politically_exposed, immediate_family_exposed,
                 
                 # Agreement
                 signed_at, ip_address, agreement_margin, agreement_account
                 , agreement_customer, agreement_crypto):
        
        # contact -----------------------
        self.email_address = email_address
        self.phone_number = phone_number
        self.street_address = street_address
        self.city = city
        self.state = state
        self.postal_code = postal_code
        self.country = country
        
        # identity ----------------------
        self.given_name = given_name
        self.middle_name = middle_name
        self.family_name = family_name
        self.date_of_birth = date_of_birth
        self.tax_id = tax_id
        self.tax_id_type = tax_id_type
        self.country_of_citizenship = country_of_citizenship
        self.country_of_birth = country_of_birth
        self.country_of_tax_residence = country_of_tax_residence
        self.funding_source = funding_source
        
        # disclosure --------------------
        self.is_control_person = is_control_person
        self.is_affiliated_exchange_or_finra = is_affiliated_exchange_or_finra
        self.is_politically_exposed = is_politically_exposed
        self.immediate_family_exposed = immediate_family_exposed
        
        # agreement ---------------------
        self.signed_at = signed_at
        self.ip_address = ip_address
        self.agreement_margin = agreement_margin
        self.agreement_account = agreement_account
        self.agreement_customer = agreement_customer
        self.agreement_crypto = agreement_crypto
        
        
    def accContact(self):
        contact_data = Contact(
            email_address = self.email_address
            , phone_number = self.phone_number
            , street_address = self.street_address
            , city = self.city
            , state = self.state
            , postal_code = self.postal_code
            , country = self.country
            )
        
        return contact_data
    
    def accIdentity(self):
        identity_data = Identity(
            given_name = self.given_name,
            middle_name = self.middle_name,
            family_name = self.family_name,
            date_of_birth = self.date_of_birth,
            tax_id = self.tax_id,
            tax_id_type = self.tax_id_type,
            country_of_citizenship = self.country_of_citizenship,
            country_of_birth = self.country_of_birth,
            country_of_tax_residence = self.country_of_tax_residence,
            funding_source = self.funding_source
            )
        return identity_data
    
    def accDisclosure(self):
        disclosure_data = Disclosures(
            is_control_person = self.is_control_person,
            is_affiliated_exchange_or_finra = self.is_affiliated_exchange_or_finra,
            is_politically_exposed = self.is_politically_exposed,
            immediate_family_exposed = self.immediate_family_exposed,
            )
        return disclosure_data
    
    def accAgreement(self):
        agreement_data = [
            Agreement(
              agreement = self.agreement_margin,
              signed_at = self.signed_at,
              ip_address = self.ip_address,
            ),
            Agreement(
              agreement = self.agreement_account,
              signed_at = self.signed_at,
              ip_address = self.ip_address,
            ),
            Agreement(
              agreement = self.agreement_customer,
              signed_at = self.signed_at,
              ip_address = self.ip_address,
            ),
            Agreement(
              agreement = self.agreement_crypto,
              signed_at = self.signed_at,
              ip_address = self.ip_address,
            )
        ]
        
        return agreement_data
    
    def addAccount(self):
        
        # id_user = getIDbyEmail(self.email_address)
        
        # if id_user in None:
        account_data = CreateAccountRequest( 
                            contact = self.accContact
                            , identity = self.accIdentity
                            , disclosures = self.accDisclosure
                            , agreements = self.accAgreement
                        )
        account = broker_client.create_account(account_data)
        
        return 'The account is created'
    


    
    

    

a = AccountData(email_address = 'test2@example.com'
              , phone_number = '555-222-333'
              , street_address = [Faker().address()]
              , city = Faker().city()
              , state = 'AL'
              , postal_code = Faker().postcode()
              , country = 'USA'
              , given_name = Faker().first_name()
              , middle_name = Faker().first_name()
              , family_name = Faker().last_name()
              , date_of_birth = "1971-01-01"
              , tax_id = '778-62-8144'
              , tax_id_type = TaxIdType.USA_SSN
              , country_of_citizenship = "USA"
              , country_of_birth = "USA"
              , country_of_tax_residence = 'USA'
              , funding_source = [FundingSource.EMPLOYMENT_INCOME]
              , is_control_person = False
              , is_affiliated_exchange_or_finra = False
              , is_politically_exposed = False
              , immediate_family_exposed = False
              , signed_at = "2022-09-11T18:09:33Z"
              , ip_address = Faker().ipv4()
              , agreement_margin = AgreementType.MARGIN
              , agreement_account = AgreementType.ACCOUNT
              , agreement_customer = AgreementType.CUSTOMER
              , agreement_crypto = AgreementType.CRYPTO)

a.addAccount()


a.accContact()
a.accIdentity()

class CreateAccount(AccountData):
    account_data = CreateAccountRequest( 
                        contact = a.accContact
                        , identity = a.accIdentity
                        , disclosures = a.accDisclosure
                        , agreements = a.accAgreement
                    )
    account = broker_client.create_account(account_data)



















