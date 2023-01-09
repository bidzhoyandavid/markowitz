# -*- coding: utf-8 -*-
"""
Created on Fri Dec 16 14:06:43 2022

@author: bidzh
"""

from dbupload.config import *

class InvalidNameError(Exception):
    def __init__(self, msg):
        self.msg = msg
    
    def __repr__(self):
        return self.msg




def getIDAccountStatus(name):
    """
        The function gets id of accountStatus
    """
    
    id_name = pd.read_sql('select id_record from users.cat_accountstatus where attribute_name = %(n)s'
                          , params = {'n': name}
                          , con = postg_engine)
    if not id_name.empty:
        return id_name.iloc[0,0]
    else:
        raise InvalidNameError("There is no {} in cat_accountstatus".format(name))
        

def getIDAccountType(name):
    """
        The function gets id of accounttype
    """
    
    id_name = pd.read_sql('select id_record from users.cat_accounttype where attribute_name = %(n)s'
                          , params = {'n': name}
                          , con = postg_engine)
    if not id_name.empty:
        return id_name.iloc[0,0]
    else:
        raise InvalidNameError("There is no {} in cat_accounttype".format(name))
        
def getIDAgreements(name):
    """
        The function gets id of agreement
    """
     
    id_name = pd.read_sql('select id_record from users.cat_agreements where attribute_name = %(n)s'
                          , params = {'n': name}
                          , con = postg_engine)
    if not id_name.empty:
        return id_name.iloc[0,0]
    else:
        raise InvalidNameError("There is no {} in cat_agreements".format(name))
        

def getIDContextType(name):
    """
        The function gets id of contexttype
    """
    
    id_name = pd.read_sql('select id_record from users.cat_contexttype where attribute_name = %(n)s'
                          , params = {'n': name}
                          , con = postg_engine)
    if not id_name.empty:
        return id_name.iloc[0,0]
    else:
        raise InvalidNameError("There is no {} in cat_contexttype".format(name))


def getIDCryptoStatus(name):
    """
        The function gets id of cryptostatus
    """
    id_name = pd.read_sql('select id_record from users.cat_cryptostatus where attribute_name = %(n)s'
                          , params = {'n': name}
                          , con = postg_engine)
    if not id_name.empty:
        return id_name.iloc[0,0]
    else:
        raise InvalidNameError("There is no {} in cat_cryptostatus".format(name))
    

def getIDDocumentType(name):
    """
        The function gets id of documenttype
    """
    id_name = pd.read_sql('select id_record from users.cat_documenttype where attribute_name = %(n)s'
                          , params = {'n': name}
                          , con = postg_engine)
    if not id_name.empty:
        return id_name.iloc[0,0]
    else:
        raise InvalidNameError("There is no {} in cat_documenttype".format(name))


def getIDEmploymentStatus(name):
    """
        The function gets id of employmentstatus
    """

    id_name = pd.read_sql('select id_record from users.cat_employmentstatus where attribute_name = %(n)s'
                          , params = {'n': name}
                          , con = postg_engine)
    if not id_name.empty:
        return id_name.iloc[0,0]
    else:
        raise InvalidNameError("There is no {} in cat_employmentstatus".format(name))
    

def getIDEnums(name):
    """
        The function gets id of enums 
    """
    id_name = pd.read_sql('select id_record from users.cat_enums where attribute_name = %(n)s'
                          , params = {'n': name}
                          , con = postg_engine)
    if not id_name.empty:
        return id_name.iloc[0,0]
    else:
        raise InvalidNameError("There is no {} in cat_enums".format(name))
      

def getIDFundingSource(name):
    """
        The function gets id of fundingSource
    """
    id_name = pd.read_sql('select id_record from users.cat_fundingsource where attribute_name = %(n)s'
                          , params = {'n': name}
                          , con = postg_engine)
    if not id_name.empty:
        return id_name.iloc[0,0]
    else:
        raise InvalidNameError("There is no {} in cat_fundingsource".format(name))
   


def getIDTaxType(name):
    """
        The function gets id of taxtype
    """
    id_name = pd.read_sql('select id_record from users.cat_taxidtype where attribute_name = %(n)s'
                          , params = {'n': name}
                          , con = postg_engine)
    if not id_name.empty:
        return id_name.iloc[0,0]
    else:
        raise InvalidNameError("There is no {} in cat_taxidtype".format(name))



def getIDVisaType(name):
    """
        The function gets id of visatype
    """
    id_name = pd.read_sql('select id_record from users.cat_visatype where attribute_name = %(n)s'
                          , params = {'n': name}
                          , con = postg_engine)
    if not id_name.empty:
        return id_name.iloc[0,0]
    else:
        raise InvalidNameError("There is no {} in cat_visatype".format(name))
    







    
    