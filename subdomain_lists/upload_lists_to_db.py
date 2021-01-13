import pandas as pd
import math 


def AddCSVToBlacklist(csvfilename):
    
    '''
    
    SAMPLE USAGE:
    
    run in Terminal:
    
    from upload_lists_to_db import *

    AddCSVToBlacklist('combined.csv')
    
    
    '''
    
    # import the data and 
    df = pd.read_csv(csvfilename)

    values = ["('"+x+"')" for x in df['name']]
    
    insert_string = ','.join(values)
    
    sql = f"INSERT INTO blacklist (name) VALUES '{insert_string}';"
                    
    executeQuery(sql)
    
    msg = f"{sql}"
    
    
def AddCSVToReserved(csvfilename):
    
    '''
    
    SAMPLE USAGE:
    
    1) download csv from https://docs.google.com/spreadsheets/d/1TjDli-ZcaS_EFLjmeISIH_X9AO5vpKNTER0TI01IzOw/edit#gid=234705264 > reserved_subdomains.csv
    
    2) run in Terminal:
    
    from upload_lists_to_db import *

    AddCSVToReserved('reserved_subdomains.csv')
    
    '''
    
    df = pd.read_csv('reserved_subdomains.csv')
    
    values = []
    
    for i in range(len(df)):
        name = df.iloc[i]['name']
        subdomain_type = df.iloc[i]['subdomain_type']
        url = df.iloc[i]['url']
        if math.isnan(url):
            url=''
        description = df.iloc[i]['description'].replace("'","\'")
        values_row = "('"+name+"','"+subdomain_type+"','"+url+"','"+description+",'12/01/2020','12/31/2999')"
        values.append(values_row)
        
    insert_string = ','.join(values)
    
    sql = f"INSERT INTO (host,type,address,description,start_date,end_date) VALUES (name,'reserved',url,description,'12/01/2020','12/31/2999') VALUES {insert_string};"
    
    executeQuery(sql)
    
    msg = f"{sql}"    