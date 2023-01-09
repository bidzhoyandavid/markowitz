# -*- coding: utf-8 -*-
"""
Created on Wed Dec 14 12:15:05 2022

@author: bidzh
"""

import pandas as pd
from sqlalchemy import create_engine



# =============================================================================
# functions
# =============================================================================


def DetectNewCountry(WebCounrtyList):
        """
        The function detects whrether there are some differences between web and db dataframes.
        And if any then insert new countries
        """
        DBCountryList  = pd.read_sql("select * from trade_data.cat_countries", con = postg_engine)
        if DBCountryList['country_name'].equals(WebCounrtyList['country_name']):
            return None
        else:
            NewCounrty = DBCountryList.merge(WebCounrtyList, how = 'outer', indicator=True)
            NewCounrty = NewCounrty[NewCounrty._merge =='right_only']
            NewCounrty = pd.DataFrame(NewCounrty['country_name'])
            NewCounrty.to_sql('cat_coutries', con=postg_engine, if_exists='append',  schema= 'trade_data' ,index=False )
            
            return '{} new country(ies) inserted'.format(len(NewCounrty))
               

def DetectNewSector(DBSectorList, WebSectorList):
    """
    The function detects whrether there are some differences between web and db dataframes.
    And if any then insert new countries
    """    
    DBSectorList = pd.read_sql("select * from trade_data.cat_sectors",   con = postg_engine)

    if DBSectorList['sector_name'].equals(WebSectorList['sector_name']):
        return None
    else:
        NewSector = DBSectorList.merge(WebSectorList, how = 'outer', indicator=True)
        NewSector = NewSector[NewSector._merge == 'right_only']
        NewSector = pd.DataFrame(NewSector['sector_name'])
        NewSector.to_sql('cat_sectors', con=postg_engine, if_exists='append',  schema= 'trade_data' ,index=False )
        
        return '{} new sector(s) inserted'.format(len(NewSector))
    
    
def DetectNewIndustry(WebindustryList):
     """
     The function detects whrether there are some differences between web and db dataframes.
     And if any then insert new countries
     """
     DBIndustryList   = pd.read_sql("select * from trade_data.cat_industries", con = postg_engine)

     
     if DBIndustryList['indusrty_name'].equals(WebindustryList['indusrty_name']):
         return None
     else:
         NewIndustry = DBIndustryList.merge(WebindustryList, how = 'outer', indicator = True)
         NewIndustry = NewIndustry[NewIndustry._merge == 'right_only']
         NewIndustry = pd.DataFrame(NewIndustry['indusrty_name'])
         NewIndustry.to_sql('cat_industries', con=postg_engine, if_exists='append',  schema= 'trade_data' ,index=False )
         
         return '{} new industry(ies) inserted'.format(len(NewIndustry))


def InsertNewCompany():
    """
    Insert new company that had been added to listing companies yesterday
    """

    result = pd.merge(all_data_final, DBcountries, how = 'inner', left_on = 'Country', right_on = 'country_name')
    result = pd.merge(result, DBsectors, how = 'inner', left_on = 'Sector', right_on = 'sector_name')
    result = pd.merge(result, DBindustry, how = 'inner', left_on = 'Industry', right_on = 'indusrty_name')
    result = result[['Symbol', 'Name', 'IPO Year', 'id_country'
                     , 'id_sector', 'id_industry', 'Exchange', 'Status']]
    result = result.rename(columns = {'IPO Year': 'IPO_Year'})
    result.columns = result.columns.str.lower()
    
    result.to_sql('cat_companies', con=postg_engine, if_exists='append',  schema= 'trade_data' ,index=False)


def UpdateStatusCompany(result):
    
    for i in result['Symbol'].index:        
        symbol = result.iloc[i, 'Symbol']
        sql = """ update trade_data.cat_companies
                  set status = 'delist'
                  where symbol = %s """
            
        cur.execute(sql, (symbol))
    
    return 'The status of delisted companies are updated'
            
