from . import routes
from xml.etree.ElementTree import fromstring, ElementTree

from flask import Flask, render_template, request, flash, redirect, url_for, session
from datetime import date, datetime, timedelta
import time
import requests

from .utils import mysql_utils as mysql
from .utils import namecheap_utils as namecheap
from .utils import stripe_utils as stripe

import logging

logging.basicConfig(level=logging.INFO)


# ROUTES
# +++++++++++++++++++++++

@routes.route('/getHosts')
def getHosts():
    # returns a list of dicts containing parsed info for all existing host records.
    
    service_url,service_url_test,api_username,api_key,api_key_test,client_ip,SLD,TLD = namecheap.namecheapCreds()
    
    url=f"https://{service_url}/xml.response?ApiUser={api_username}&ApiKey={api_key}&UserName={api_username}&ClientIp={client_ip}&Command=namecheap.domains.dns.getHosts&SLD={SLD}&TLD={TLD}"
    response = requests.get(url)
    tree = ElementTree(fromstring(response.content))
    root = tree.getroot().find('{http://api.namecheap.com/xml.response}CommandResponse')

    #parse Namecheap API XML response
    hosts=[]
    result={}
    for child in root.iter('{http://api.namecheap.com/xml.response}host'):
        host_name=child.attrib['Name']
        host_type=child.attrib['Type']
        host_address=child.attrib['Address']
        host_ttl=child.attrib['TTL']
        result={'Name':host_name
               ,'Type':host_type
               ,'Address':host_address
               ,'TTL':host_ttl}
        hosts.append(result)
        
    return url

@routes.route('/test/<host_name>')
def test(host_name):
    
    user_id = 3
    host_type = 'URL'
    address = 'www.reddit.com'
    description = 'testing 123123'
    datetime_requested = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    start_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    end_date = datetime.now() + timedelta(minutes=10)
    end_date = end_date.strftime("%Y-%m-%d %H:%M:%S")

    
    results = mysql.getQueryResults(f"SELECT * from hosts where host_name='{host_name}'")
    
    #if host_name is not already in hosts table, add a new row so it has an id we can insert into the subscriptions table
    if len(results)==0:
        
        
        hosts_sql = f"INSERT INTO hosts (user_id,host_name, subdomain_group, description, datetime_requested, start_date, end_date, is_active, is_requested, is_premium) VALUES ({user_id},'{host_name}','pending review','pending review','{datetime_requested}','{start_date}','{end_date}',true,true,false);"
        
        mysql.executeQuery(hosts_sql)
        
        new_host_id = mysql.getQueryResults(f"SELECT * from hosts where host_name = '{host_name}'")[0]['id']
        
    else:   
        
        msg = ''
                
        new_host_id = results[0]['id']
        
        hosts_sql = f"UPDATE hosts SET user_id={user_id},is_requested=true,datetime_requested='{datetime_requested}',start_date='{start_date}',end_date='{end_date}',is_active=true where host_name = '{host_name}';"
            
        mysql.executeQuery(hosts_sql)
        
    host_request_sql = f"INSERT INTO host_requests (host_id, user_id, host_name, type, address, datetime_requested, description, payment_status) VALUES ({new_host_id}, {user_id}, '{host_name}', '{host_type}', '{address}', '{description}','{datetime_requested}', 'new request');"
            
    subscriptions_1 = f'''
                        INSERT INTO subscriptions 
                        (host_id, host_name, start_date, end_date, is_active, is_premium) 
                        SELECT id as host_id, 
                                host_name, 
                                null, 
                                null, 
                                1, 
                                is_premium 
                        FROM hosts 
                        WHERE host_name = '{host_name}';
                        '''
    
    subscriptions_2 = f'''
                        UPDATE subscriptions 
                        SET user_id = {user_id}, 
                            address = '{address}', 
                            type = '{host_type}',  
                            description = '{description}',
                            start_date = '{start_date}', 
                            end_date = '{end_date}'
                        WHERE host_name = '{host_name}';
                        '''
    
    logging.info("adding new subscription...")
    mysql.executeQuery(subscriptions_1)
    mysql.executeQuery(subscriptions_2)
                    
                    
    url = namecheap.setHostsURLFromDb()
    
    #resp = requests.post(url)
                
    #return f"Added {host_name} starting at {start_date} and ending at {end_date}"
    
    return url
                
                

#This runs after confirming payment via stripe

def confirmSubscription():    
    subscriptions_sql = f"INSERT INTO subscriptions (host_id, name, is_active, is_premium) VALUES ({host_id}, '{host_name}', 0, {is_premium});"
    
    start_date = datetime.now()
    end_date = datetime.now() + timedelta(days=364)
    hosts_sql1 = f"UPDATE hosts SET is_active = 1, start_date = {start_date}, end_date = {end_date}, last_updated_at = {start_date} WHERE host_name = '{host_name}';"
    
    #update DNS