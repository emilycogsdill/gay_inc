
'''
user_management.py
contains routes for login, logout, account creation, password change/reset
basically anything a user would do that doesn't involve subdomains

Routes:

/request-password-reset
/reset-password/<token>
/login
/register
/account
/logout
/change_or_reset_password

'''

from . import routes

from flask import Flask, render_template, request, flash, redirect, url_for, session, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from sqlalchemy import or_, func, create_engine, Table, Column, Integer, String, MetaData, ForeignKey, inspect
from sqlalchemy.sql import text
import mysql.connector #requires mysql-connector-python
from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, RadioField, HiddenField, StringField, IntegerField, FloatField, validators
from wtforms.validators import InputRequired, Length, Regexp, NumberRange, DataRequired

from flask_mail import Mail, Message
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

from flask import Blueprint

# ROUTES
# +++++++++++++++++++++++


@routes.route('/request-password-reset', methods=['GET', 'POST'])
def request_password_reset():
    
    if request.method == 'POST' and 'email' in request.form:
        
        email = request.form['email']
        
        #TODO: validate that email is associated with an account
        username = mysql.GetUsernameFromEmail(email)
            
        if len(username)==0:
            alert = f"No users found with email address {email}. Try that again maybe?"
            return render_template('request_password_reset.html', msg = alert, session = session)
        
        token = get_reset_token(username)
        
        recipient_email = email
        
        msg = Message()
        msg.subject = "Flask App Password Reset"
        msg.sender = environ['GAY_EMAIL_USERNAME']
        msg.recipients = [recipient_email]
        reset_url = f"https://is.gay//reset-password/{token}"
        msg.html = f"Hey! Looks like you requested a password reset for username <b>{username}</b> on is.gay. Follow <a href='{reset_url}'>this link</a> to reset your account password. Try not to lose it this time!!!<p>If you did NOT mean to reset your password, well, that's not great! Contact us at gay@is.gay and we will sort it out."
        mail.send(msg)
    
        alert = f"Password reset instructions have been emailed to {recipient_email}."
    
        return render_template('request_password_reset.html', msg = alert, session = session)
    
    elif request.method == 'POST':
        alert = "You need to give us an email for us to do anything bruh"
        
    else:
        alert = "To request a password reset link, enter the email address associated with your account below."
        
    return render_template('request_password_reset.html', msg = alert, session = session)



@routes.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    
    try:
        username = jwt.decode(token, key=environ['SECRET_KEY_FLASK'], algorithms=["HS256"])['reset_password']
        msg = f"What's up {username}? Here to reset your password? It do be like that sometimes"
    
    #except ExpiredSignatureError:
    except:
        alert = "Something went wrong. Maybe your token expired? RIP anyway try again"
        return render_template('request_password_reset.html', msg = alert, session = session)
        
    if request.method == 'POST' and 'new_password' in request.form and 'confirm_new_password' in request.form:
        
        new_password = request.form['new_password']
        confirm_new_password = request.form['confirm_new_password']
                   
        if new_password!=confirm_new_password:
            
            msg = "Passwords need to match!! It's REALLY not that hard"
        #TODO: add some password validation
        
        else:
            try:
                sql = f"""
                UPDATE users 
                SET password=MD5('{new_password}') WHERE username='{username}'
                """
                mysql.executeQuery(sql)
                
                # Remove session data, this will log the user out
                session.pop('loggedin', None)
                session.pop('id', None)
                session.pop('username', None)
                
                msg = "Password successfully reset - give it a whirl?"
                
                return render_template('login.html', msg_after_reset = msg, session = session)
                
            except:
                
                msg = "ur sql is bad and you should feel bad"
                           
        
    elif request.method == 'POST':
        
        msg = "If you don't fill out the form there's not a whole lot we can do about that"
        
    return render_template('reset-password.html', token = token, msg = msg, session = session)

    
    
    

@routes.route('/login', methods=['GET', 'POST'])
def login():
    # Output message if something goes wrong...
    msg = ''
    
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
    
        # Check if account exists using MySQL
        sql = f"SELECT * FROM users WHERE username = '{username}' and password = MD5('{password}') LIMIT 1;"
        
        results = mysql.getQueryResults(sql)
        
        # If account exists in users table in our database
        if results:
            
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            login = True
            
            session['id'] = results[0]['id']
            session['username'] = results[0]['username']
            session['email'] = results[0]['email']        
            
            # Redirect to home page
            return render_template('home.html', username = session['username'], msg = '', session = session)
    
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'

    return render_template('login.html', msg = msg, session = session)



@routes.route('/logout')
def logout():
    
    # Remove session data, this will log the user out
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    
    # Redirect to login page
    return redirect(url_for('routes.login'))



@routes.route('/register', methods=['GET', 'POST'])
def register():
    
    msg = ''
    
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        user_created_datetime = datetime.now()      
        
        try:
            first_name = request.form['first_name']
        except:
            first_name = ''
        try:
            last_name = request.form['last_name']
        except:
            last_name = ''
        
        # If account exists show error
        if mysql.getQueryResults(f"SELECT * FROM users WHERE username = '{username}'"):
            msg = 'Account with that username already exists!' #TODO: password reset
        elif mysql.getQueryResults(f"SELECT * FROM users WHERE email='{email}'"):
            msg = 'Account with that email address already exists!' #TODO: password reset
        # Form validation
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address :('
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers :('
        elif not username or not password or not email:
            msg = "Please fill out the form :( It's REALLY not that hard"
        else:
            sql = f"INSERT INTO users (user_created_datetime, username, password, email, first_name, last_name) VALUES ('{user_created_datetime}','{username}', MD5('{password}'), '{email}','{first_name}','{last_name}');"
            
            mysql.executeQuery(sql)
            
            #Create a customer in Stripe
            customer_id = stripe.createCustomer(email,username)
            
            mysql.executeQuery(f"""UPDATE users SET stripe_customer_id='{customer_id}' WHERE username='{username}'""")
            
            session['username'] = username
            session['email'] = email
            session['id'] = mysql.GetUserIDFromUsername(username)
            session['loggedin'] = True       
            session['newuser'] = True         
            
            # Redirect to home page
            return render_template('home.html', username = username, msg = '', login = True, session = session)
        
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
        
    # Show registration form with message (if any)
    return render_template('register.html', msg = msg, session = session)



@routes.route('/account', methods=['GET','POST'])
def account():
    
    if 'loggedin' not in session:
        return redirect(url_for('routes.login'))

    else:
        
        username = session['username']
        account_sql = f"SELECT * FROM users WHERE username = '{username}'"
        account_results = mysql.getQueryResults(account_sql)
        
        return render_template('account.html', account = account_results, session = session)

        
        
@routes.route('/change_or_reset_password', methods=['GET', 'POST'])
def change_or_reset_password():
    
    msg = ''
    
    if 'loggedin' in session:
        
        username = session['username']
        
        msg = f"What's up {username}? Here to change your password? Fine, I guess"
        
        if request.method == 'POST' and 'old_password' in request.form and 'new_password' in request.form:
        
            old_password = request.form['old_password']
            new_password = request.form['new_password']
                       
            if mysql.authenticate(username,old_password) and old_password==new_password:
                
                msg = "It would help a lot if your new password were a different one"

            elif mysql.authenticate(username,old_password):

                try:
                    sql = f"""
                    UPDATE users 
                    SET password=MD5('{new_password}') WHERE username='{username}'
                    """
                    
                    mysql.executeQuery(sql)
                    
                    msg = "Updated password successfully!"
                    
                except:
                    
                    msg = "ur sql is bad and you should feel bad"
                
            
            else:
                
                msg=f"Incorrect password for user {username}. Try again? Or maybe you want to RESET your password?"
                
            
        elif request.method == 'POST':
            
            msg = "If you don't fill out the form there's not a whole lot we can do about that"

        return render_template('change-or-reset-password.html', msg = msg, session = session)
                     
    else:       
        return redirect(url_for('routes.login'))