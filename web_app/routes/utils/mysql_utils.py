from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_, func, create_engine, Table, Column, Integer, String, MetaData, ForeignKey, inspect
from sqlalchemy.sql import text
import mysql.connector #requires mysql-connector-python
from os import environ


def createEngine():
    username = environ['DB_USERNAME']
    password = environ['DB_PASSWORD']
    hostname = environ['DB_HOSTNAME']
    database = environ['DB_DATABASE']
    
    #api_secret_prod = environ['STRIPE_SECRET_KEY']
    
    SQLALCHEMY_DATABASE_URI = f'mysql+mysqlconnector://{username}:{password}@{hostname}/{database}'
    
    engine = create_engine(SQLALCHEMY_DATABASE_URI)
    
    return engine

def executeQuery(sql):
    
    engine = createEngine()
    
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
    sql = f"SELECT * FROM users WHERE username = '{username}'"

    try:
        results = getQueryResults(sql)
        account = results[0]
        user_id = account['id']
    except:
        user_id = ''
        
    return user_id

def GetUsernameFromEmail(email):
    sql = f"SELECT * FROM users WHERE email = '{email}'"

    try:
        results = getQueryResults(sql)
        account = results[0]
        username = account['username']
    except:
        username = ''
        
    return username


def authenticate(username,password):
    #returns True if username and password match record in database    
    
    with engine.connect() as con:
            rs = con.execute(f"""
                            SELECT * 
                            FROM users 
                            WHERE username = '{username}'
                            AND password = MD5('{password}') LIMIT 1;
                            """)
    
    results = [dict(zip(row.keys(), row)) for row in rs]
    
    # If account exists in users table in our database
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
                             JOIN users ON hosts.user_id=users.id
                             WHERE users.username = '{username}' 
                             AND host = '{host}';
                             """)
    
    results = [dict(zip(row.keys(), row)) for row in rs]
    
    # If account exists in users table in our database
    if results:
        return True
    
    else:
        return False
    
    
def getAccount(session):
    
    sql = f"SELECT * FROM users WHERE username = '{session['username']}'"
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
    
    account_sql = f"SELECT * FROM users WHERE username = '{username}'"
    results = getQueryResults(account_sql)
    account = results[0]
    
    host_detail_sql = f"""SELECT users.username, hosts.* 
                        FROM hosts 
                        JOIN users on hosts.user_id=users.id
                        WHERE hosts.host= '{host}'
                        """
    host_detail_results = getQueryResults(host_detail_sql)
    
    try:
        results = host_detail_results[0]
    
    except:
        results = []
    
    return results