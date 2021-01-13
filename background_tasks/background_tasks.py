#!/usr/bin/python3
"""
Background process runs to continually update the namecheap DNS to reflect the contents of the subscriptions table
(only records where start_date < now and end_date > now)
"""
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_, func, create_engine, Table, Column, Integer, String, MetaData, ForeignKey, inspect
from sqlalchemy.sql import text
import mysql.connector #requires mysql-connector-python
from os import environ
from datetime import datetime


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

def setHostsURLFromDb():
    #returns a URL that will make the API call to update DNS to reflect contents of "hosts" table in MySQL
    
    #get creds from environ variables
    service_url,service_url_test,api_username,api_key,api_key_test,client_ip,SLD,TLD = namecheapCreds()
    
    #get existing hosts from MySQL
    sql = '''
            SELECT host_name, type, address 
            FROM subscriptions 
            WHERE is_active=true;
          '''
    
    hosts = getQueryResults(sql)
    
    #construct a URL from this dict
    commands=[]
    i=1
    
    for elem in hosts:
        HostNameParam='HostName'+str(i)
        RecordTypeParam='RecordType'+str(i)
        AddressParam='Address'+str(i)
        TTLParam='TTL'+str(i)
        i+=1
        HostName=elem['host_name']
        RecordType=elem['type']
        Address=elem['address']
        TTL=60
        command_string=f"&{HostNameParam}={HostName}&{RecordTypeParam}={RecordType}&{AddressParam}={Address}&{TTLParam}={TTL}"
        commands.append(command_string)
            
    command_parameters=''.join(commands)
    
    url_base=f"https://{service_url}/xml.response?ApiUser={api_username}&ApiKey={api_key}&UserName={api_username}&ClientIp={client_ip}&"
    
    url_command=f"Command=namecheap.domains.dns.setHosts&SLD={SLD}&TLD={TLD}"
    
    url=url_base + url_command + command_parameters
    
    return url 
    
    

def tasks():
    
    sql = '''
            INSERT INTO test (timestamp) SELECT NOW();
          '''
    executeQuery(sql)
    
    """
    Update the `is_active` flags based on start and end timestamps
    """
    
    sql = '''
            SELECT 1
            --this is SQL I don't want you to see :)
          '''
    executeQuery(sql)
    
    """
    update DNS to reflect current state of the subscriptions table
    (this allows us to have users test new subdomains by creating a new subscription record when they register an auto-approved domain, but set the end_date timestamp to be only a half hour after it started)
    """
    url = namecheap.setHostsURLFromDb()
    resp = requests.post(url)
    
    timestamp = datetime.now()

sched = BackgroundScheduler(daemon=True)
sched.add_job(tasks,'interval',seconds=60)
sched.start()

app = Flask(__name__)

application = app

@app.route("/")
def schedulertest():
    return f"great job"

if __name__ == "__main__":
    app.run()