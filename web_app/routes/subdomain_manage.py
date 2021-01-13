from . import routes

from flask import Flask, render_template, request, flash, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from sqlalchemy import or_, func, create_engine, Table, Column, Integer, String, MetaData, ForeignKey, inspect
from sqlalchemy.sql import text
import mysql.connector #requires mysql-connector-python
from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, RadioField, HiddenField, StringField, IntegerField, FloatField, validators
from wtforms.validators import InputRequired, Length, Regexp, NumberRange, DataRequired

from flask_mail import Mail, Message
from flask import current_app

import jwt

from datetime import date,datetime
import random
import itertools
from os import environ
import re
import requests
import sys
import time

from .utils import mysql_utils as mysql
from .utils import namecheap_utils as namecheap
from .utils import stripe_utils as stripe

    
# ROUTES
# +++++++++++++++++++++++


@routes.route('/')
@routes.route('/home')
def home():
    if 'loggedin' in session:
        login = True
        msg = ''
        username = session['username']
        if 'newuser' in session:
            msg = f"Thank you for registering, {username}! Proud of u."
            session.pop('newuser', None)
        else:
            msg = f"Welcome back, {username}!"
            
    else:
        login = False
        username=''
        msg = """Welcome to the gayest timeline! We sell gay subdomains. Like this: <yoursubdomain>.is.gay - wowee!"""
        
    
    return render_template('home.html', username = username, msg = msg, session = session)
   

        
# add a new domain!
@routes.route('/newdomain-old', methods=['GET', 'POST'])
def newdomain_old():
    
    msg = ''
    
    if 'loggedin' in session:
        
        username = session['username']
        
        msg = f"What's up {username}? Here to add a new domain? You better be! That's what you do here."
        
        if request.method == 'POST' and 'host' in request.form and 'host_type' in request.form and 'address' in request.form and 'password' in request.form:
        
            host_name = request.form['host_name']
            host_type = request.form['host_type']
            address = request.form['address']
            password = request.form['password']
            #TODO: add these with form validation
            #start_date = request.form['start_date']
            #end_date = request.form['end_date']
            datetime_requested = datetime.now()
            start_date = '12/01/2020'
            end_date = '12/01/2021'
                    
            results = mysql.getQueryResults(f"SELECT * from hosts where host_name='{host_name}'")
            
            
            #check for successful authentication first
            if not mysql.authenticate(username,password):
                msg=f"Incorrect password for user {username}. Try again? Please?"
            
            
            
            #request goes through iff the subdomain is 1) whitelisted and 2) not yet active
            #request will succeed if subdomain has been requested (is_requested=true) but not active. This means the other user has not yet submitted payment
            elif results['subdomain_group']=='whitelist' and results['is_active']==0:
                #get the user id
                username = session['username']
                user_id = session['id']
                
                try:
                    
                    host_request_1 = f"INSERT INTO host_requests (user_id, host_name, type, address, datetime_requested, payment_status) VALUES ({user_id}, '{host_name}', '{host_type}', '{address}', '{datetime_requested}', 'new request');"
                    
                    host_request_2 = f"UPDATE host_requests SET host_id = {results['subdomain_group']} WHERE host_name={host_name};"
                    
                    subscriptions_1 = f"INSERT INTO subscriptions (host_id, name, start_date, end_date, is_active, is_premium) SELECT id as host_id, host as name, null, null, 0, is_premium FROM hosts WHERE host_name={host_name};"
                    
                    subscriptions_2 = f"UPDATE subscriptions SET user_id = {user_id} WHERE host_name = {host_name};"
                    
                    hosts_1 = f"UPDATE hosts SET user_id = {user_id} WHERE host_name = {host_name};"

                    hosts_2 = f"UPDATE hosts SET is_requested = true WHERE host_name = {host_name};"                    
                    
                    queries = host_request_1 + host_request_2 + subscriptions_1 + subscriptions_2 + hosts_1 + hosts_2
                    
                    mysql.executeQuery(queries)
                    
                    msg = f"Requested host_name={host_name} with host_type={host_type} at address={address}. Great job! Keep going!!! YOUR VENGEFUL GOD DEMANDS MORE"
                    
                except:
                    msg = "ur sql is bad and you should feel bad"
                    
            elif results['subdomain_group']=='blacklist':
                msg=f"Host name {host_name} violates our policies for subdomain naming. Probably it is a famous person or something! That's not super chill! Try something more fun?"
                
            elif results['is_active']==1 or results['subdomain_group']==1:
                msg=f"Host name {host_name} is not available :(. Try something more gay?"
            
            elif len(results)==0:
                msg=f"Host name {host_name} is not on our list of automatically-approved subdomains. Please submit a request HERE. ....eventually there will be a link lol"
            
            
                    
        elif request.method == 'POST':
            msg = "If you don't fill out the form there's not a whole lot we can do about that"

        return render_template('newdomain.html', msg = msg, session = session)    
    
    #if user not logged in, redirect to login page
    else:
        return redirect(url_for('routes.login'))
                
                
                
    
    '''

#We aren't quite ready for this


# add a new domain!
@routes.route('update-dns', methods=['GET', 'POST'])
def update_DNS():    
    
    msg = ''
    
    if 'loggedin' in session:
        
        username = session['username']
        
        #update DNS
               
        try:
            
            #Now that the new record is in the database, we can do a select * on the table and use that to update the DNS config
                    url = setHostsURLFromDb()

                    resp = requests.post(url)
                    
                    if resp.status_code == 200:
                        msg = f"Added host_name={host_name} with host_type={host_type} at address={address}. Great job! Keep going!!! YOUR VENGEFUL GOD DEMANDS MORE"
                    
                    else:
                        msg = "Namecheap API fail sry"
                    
                except:
                    msg = "Failed to update DNS, it's not super clear why sry I'm bad at raising error messages"
            
        elif request.method == 'POST':
            msg = "If you don't fill out the form there's not a whole lot we can do about that"

        return render_template('newdomain.html', msg = msg, session = session) #, username=session['username'], msg = msg, session = session)
    
    
    #if user not logged in, redirect to login page
    else:
        return redirect(url_for('routes.login'))
'''
    
@routes.route('/subdomain-for-sale')
def subdomain_for_sale():
    
    msg = "That subdomain is available! You can buy it! wow!"
        
    return render_template('home.html', msg = msg, session = session, newsubdomain = True)


@routes.route('/info')
def info():
    return render_template('info.html', session = session)

#@routes.route('/detail/{host_name}')
#def detail(host):

@routes.route('/detail/<host>')
def detail(host):
    
    if 'loggedin' in session:

        try:
            host_details=mysql.getHostDetails(session,host)

            if session['username'] != host_details['username']:
                msg = f"{host_name} is a thing, but it's not your thing! Shoo shoo!"
                
            elif session['username'] == host_details['username']:
                msg = f"What's up {session['username']}, want to learn more about your subdomain {host_name}? Too bad, we aint there yet"
                
        except IndexError:
            msg = f"There doesn't seem to be anything here? You have a janky URL? Fake news???"
        
        return render_template('detail.html', msg = msg, session = session, host = host)
        
        
    else:
        return redirect(url_for('routes.login'))
    
    
    
@routes.route('/my-subdomains')
def my_subdomains():
    
    if 'loggedin' not in session:
        return redirect(url_for('routes.login'))

    else:
        
        return render_template('my-subdomains.html', account = mysql.getAccount(session), hosts = mysql.getHostData(session), msg = '', session = session)
    

@routes.route('/remove/<host>')
def remove_host(host):
    
    if 'loggedin' in session:
    
        login = True
        
        username = session['username']
        
        user_id = mysql.GetUserIDFromUsername(username)
        
        if mysql.confirmUserOwnsHost(username,host):
            msg = f"Are you sure you want to delete {host_name}? Really really sure? That's what you want? For real?"
            return render_template('remove.html', msg = msg, session = session, host = host)

        else:            
            msg = f"{host_name} is not yours to delete! Go find something else to do!!"
            
            return render_template('home.html', msg = msg, session = session)
                     
    else:       
        
        html_template = 'layout-logged-out.html'
        
        return redirect(url_for('routes.login'))
        
    
    
@routes.route('/remove-final/<host>')
def remove_final(host):

    if 'loggedin' in session:
        
        login = True
        html_template = 'layout.html'
    
        username = session['username']
        
        if mysql.confirmUserOwnsHost(username,host):
            
            try:
                mysql.executeQuery(f"DELETE FROM hosts WHERE host_name='{host_name}';")
                msg = f"Deleted host {host_name}. I hope you're happy."
            
            except:
                msg = "ur sql is bad and you should feel bad"

        else:            
            
            msg = f"{host_name} is not yours to delete! Go find something else to do!!"
            
            return render_template('home.html', msg = msg, session = session, )
         
        
        return render_template('my-subdomains.html', account = mysql.getAccount(session), hosts = mysql.getHostData(session), msg = msg, session = session)
    
    else:       

        login = False
        html_template = 'layout-logged-out.html'
        
        return redirect(url_for('routes.login'))