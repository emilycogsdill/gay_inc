from . import routes

from flask import Flask, render_template, request, flash, redirect, url_for, session
from datetime import date, datetime, timedelta
import time

from .utils import mysql_utils as mysql
from .utils import namecheap_utils as namecheap
from .utils import stripe_utils as stripe

import requests

def lookupHostStatus(host_name):
    results = mysql.getQueryResults(f"SELECT * from hosts where host_name='{host_name}'")

    if len(results)==0:
        return 'unlisted'
    
    elif results[0]['is_available']==1:
        return 'available'
    
    else:
        return 'not available'

# ROUTES
# +++++++++++++++++++++++

@routes.route('/hostLookup', methods=['GET', 'POST'])
def hostLookup():
    msg = 'Look up whether a host is available. Cmon, try it'
    
    if request.method == 'POST' and 'host_name' in request.form:
        
        host_name = request.form['host_name']
        
        host_status = lookupHostStatus(host_name)
        
        results = mysql.getQueryResults(f"SELECT * from hosts where host_name='{host_name}'")
        
        #msg = f"{host_status}"
        if host_status=='available':
            msg = f"{host_name}.is.gay is eligible for automatic approval! 'Tis a blessed day indeed"
           
        elif host_status=='unlisted':
            msg = f"{host_name}.is.gay is not eligible for automatic approval. But it could be okay, maybe! Please send us a request."
       #
        else:
            msg = f"{host_name}.is.gay is not available. {status} Try another one!"
        
    return render_template('check-availability.html', lookup_msg = msg, session = session)  




# add a new domain!
@routes.route('/newdomain', methods=['GET', 'POST'])
def newdomain():
    
    success_msg = ""
    error_msg = ""
    
    #if user not logged in, redirect to login page
    if 'loggedin' not in session:
        return redirect(url_for('routes.login'))
    
    else:
        username = session['username']
        
        if request.method == 'POST':
            
            host_name = request.form['host_name']
            host_type = request.form['host_type']
            address = request.form['address']
            password = request.form['password']
            description = request.form['description']
            datetime_requested = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            start_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            end_date = datetime.now() + timedelta(minutes=10)
            end_date = end_date.strftime("%Y-%m-%d %H:%M:%S")                    
            
            #Step 1: Authenticate
            if not mysql.authenticate(username,password):
                
                error_msg = f"Incorrect password for user {username}. Try again? Please?"
                
                return render_template('newdomain.html', error_msg = error_msg, success_msg = success_msg, session = session)
            
            #Step 2: check to see if requested host_name is present in the hosts table. (If it doesn't exist, user will be directed to submit a request for it to be reviewed manually)
            
            user_id = mysql.GetUserIDFromUsername(username)
            
            results = mysql.getQueryResults(f"SELECT * from hosts where host_name='{host_name}'")
    
            #if host_name is not already in hosts table, add a new row so it has an id we can insert into the subscriptions table
            if len(results)==0:
                    
                hosts_sql = f"INSERT INTO hosts (user_id,host_name, subdomain_group, description, datetime_requested, start_date, end_date, is_active, is_requested, is_premium) VALUES ({user_id},'{host_name}','pending review','pending review','{datetime_requested}','{start_date}','{end_date}',true,true,false);"
                
                mysql.executeQuery(hosts_sql)
                
                new_host_id = mysql.getQueryResults(f"SELECT * from hosts where host_name = '{host_name}'")[0]['id']
               
            
            elif results[0]['is_active']==1 or results[0]['subdomain_group']=='blacklist':
                
                error_msg=f"Host name {host_name} is not available :(. Try something more gay?"
                
                return render_template('newdomain.html', error_msg = error_msg, success_msg = success_msg, session = session)
            
            else:
                        
                new_host_id = results[0]['id']
                
                hosts_sql = f"UPDATE hosts SET user_id={user_id},is_requested=true,datetime_requested='{datetime_requested}',start_date='{start_date}',end_date='{end_date}',is_active=true where host_name = '{host_name}';"
                    
                mysql.executeQuery(hosts_sql)
            
                    
            #update subscriptions table    
            subscriptions_1 = f"""
                                INSERT INTO subscriptions 
                                (host_id, host_name, is_active, is_premium) 
                                SELECT id as host_id, 
                                        host_name, 
                                        1, 
                                        is_premium 
                                FROM hosts 
                                WHERE host_name = '{host_name}';
                                """
            
            subscriptions_2 = f"""
                                UPDATE subscriptions 
                                SET user_id = {user_id}, 
                                    address = '{address}', 
                                    type = '{host_type}',  
                                    description = '{description}',
                                    start_date = '{start_date}', 
                                    end_date = '{end_date}',
                                    last_updated_at = '{start_date}'
                                WHERE host_name = '{host_name}';
                                """
            
            mysql.executeQuery(subscriptions_1)
            mysql.executeQuery(subscriptions_2)
                            
            url = namecheap.setHostsURLFromDb()
            
            resp = requests.post(url)
            
            success_msg = f"Added {host_name}. Go check it out and see if it works! This is a trial period ending at {end_date}."
            error_msg = ""
                
        else:
            success_msg = ""
            error_msg = ""
            
        return render_template('newdomain.html', error_msg = error_msg, success_msg = success_msg, session = session) 