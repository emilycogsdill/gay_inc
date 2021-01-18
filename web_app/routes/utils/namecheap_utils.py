import requests
from xml.etree.ElementTree import fromstring, ElementTree
from os import environ

import sys
sys.path.append('/home/isgasygd/dev/routes/utils')

from mysql_utils import *

#get creds

# Namecheap

def namecheapCreds():
    service_url = environ['NAMECHEAP_SERVICE_URL']
    service_url_test = environ['NAMECHEAP_SERVICE_URL_TEST']
    api_username = environ['NAMECHEAP_USERNAME']
    api_key = environ['NAMECHEAP_API_KEY']
    api_key_test = environ['NAMECHEAP_API_KEY_TEST']
    client_ip = environ['NAMECHEAP_CLIENT_ID']
    
    #change these when the time is right
    SLD = 'is'
    TLD = 'gay'
    
    return service_url,service_url_test,api_username,api_key,api_key_test,client_ip,SLD,TLD


def getHosts():
    # returns a list of dicts containing parsed info for all existing host records.
    
    service_url,service_url_test,api_username,api_key,api_key_test,client_ip,SLD,TLD = namecheapCreds()
    
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
        
    return hosts


def setHostsURLFromDb():
    #returns a URL that will make the API call to update DNS to reflect contents of "hosts" table in MySQL
    
    #get creds from environ variables
    service_url,service_url_test,api_username,api_key,api_key_test,client_ip,SLD,TLD = namecheapCreds()
    
    #get existing hosts from MySQL
    sql = '''
            SELECT host_name, type, address 
            FROM subscriptions 
            WHERE start_date<DATE_ADD(current_timestamp(), INTERVAL -1 HOUR) 
            AND end_date>DATE_ADD(current_timestamp(), INTERVAL -1 HOUR);
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