from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_, func, create_engine, Table, Column, Integer, String, MetaData, ForeignKey, inspect
from sqlalchemy.sql import text
import mysql.connector #requires mysql-connector-python
from os import environ
import pandas as pd
import math


username = environ['DB_USERNAME']
password = environ['DB_PASSWORD']
hostname = environ['DB_HOSTNAME']
database = environ['DB_DATABASE']

#api_secret_prod = environ['STRIPE_SECRET_KEY']

SQLALCHEMY_DATABASE_URI = f'mysql+mysqlconnector://{username}:{password}@{hostname}/{database}'

engine = create_engine(SQLALCHEMY_DATABASE_URI)

def executeQuery(sql):
    
    with engine.connect() as con:
        con.execute(sql)

        
def getQueryResults(sql):
    
    try:
        with engine.connect() as con:
            rs = con.execute(sql)
        
        results = [dict(zip(row.keys(), row)) for row in rs]
    
    except:
        results = []
        
    return results


def GetUserIDFromUsername(username):
    sql = f"SELECT * FROM accounts WHERE username = '{username}'"

    try:
        results = getQueryResults(sql)
        account = results[0]
        user_id = account['id']
    except:
        user_id = ''
        
    return user_id



def authenticate(username,password):
    #returns True if username and password match record in database    
    
    with engine.connect() as con:
            rs = con.execute(f"""
                            SELECT * 
                            FROM accounts 
                            WHERE username = '{username}'
                            AND password = MD5('{password}') LIMIT 1;
                            """)
    
    results = [dict(zip(row.keys(), row)) for row in rs]
    
    # If account exists in accounts table in our database
    if results:
        return True
    
    else:
        return False
    


def confirmUserOwnsHost(username,host):
    #returns True if username matches host in database    
    
    with engine.connect() as con:
            rs = con.execute(f"""
                             SELECT hosts.* 
                             FROM hosts 
                             JOIN accounts ON hosts.user_id=accounts.id
                             WHERE accounts.username = '{username}' 
                             AND host = '{host}';
                             """)
    
    results = [dict(zip(row.keys(), row)) for row in rs]
    
    # If account exists in accounts table in our database
    if results:
        return True
    
    else:
        return False
    
    
def getAccount(session):
    
    sql = f"SELECT * FROM accounts WHERE username = '{session['username']}'"
    results = getQueryResults(sql)
    
    try:
        account = results[0]

    except:
        account = []
        
    return account



def getHostData(session):
    
    sql = f"SELECT * FROM hosts WHERE user_id = '{session['id']}'"
    results = getQueryResults(sql)
    
    return results




def getHostDetails(session,host):
    
    username = session['username']
    
    account_sql = f"SELECT * FROM accounts WHERE username = '{username}'"
    results = getQueryResults(account_sql)
    account = results[0]
    
    host_detail_sql = f"""SELECT accounts.username, hosts.* 
                        FROM hosts 
                        JOIN accounts on hosts.user_id=accounts.id
                        WHERE hosts.host= '{host}'
                        """
    host_detail_results = getQueryResults(host_detail_sql)
    
    try:
        results = host_detail_results[0]
    
    except:
        results = []
    
    return results

def AddNamesToTable(db_table_string,path_to_csv):
        
    '''
    
    SAMPLE USAGE:
    
    run in Terminal:
    
    from mysql_utils import *
    AddNamesToTable('blacklist','blacklist/actor_names.csv') 
    
    '''
    
    # import the data and 
    df = pd.read_csv(path_to_csv)

    values = ["('"+x+"')" for x in df['name']]
    
    insert_string = ','.join(values)
    
    staging_table = db_table_string+'_stg'
    
    sql = f'''
    INSERT INTO {staging_table} (name) VALUES '{insert_string}';
    INSERT INTO {db_table_string}
    SELECT * FROM {staging_table} WHERE name NOT IN (SELECT * FROM {db_table_string})
    ;
    '''
                    
    executeQuery(sql)
    
    print(f"names in {path_to_csv} have been added to {db_table_string})")
    
