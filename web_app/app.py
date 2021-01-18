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

from routes import *
import logging

import sys
sys.path.append('/home/isgasygd/dev/routes/utils')

from mysql_utils import *
from background_tasks import *


# BACKGROUND TASKS
# +++++++++++++++++++++++
from apscheduler.schedulers.background import BackgroundScheduler

sched = BackgroundScheduler(daemon=True)
sched.add_job(trackExecutions,'interval',seconds=300)
sched.add_job(updateSubscriptionActiveStatus,'interval',seconds=300)
sched.add_job(updateDNS,'interval',seconds=300)
sched.add_job(updateStripeEvents,'interval',seconds=300)
sched.start()


# CREATE FLASK
# +++++++++++++++++++++++

app = Flask(__name__)


# ENVIRONMENT VARIABLES
# +++++++++++++++++++++++

# MYSQL creds
username = environ['DB_USERNAME']
password = environ['DB_PASSWORD']
hostname = environ['DB_HOSTNAME']
database = environ['DB_DATABASE']

SQLALCHEMY_DATABASE_URI = f'mysql+mysqlconnector://{username}:{password}@{hostname}/{database}'

# Namecheap
service_url = environ['NAMECHEAP_SERVICE_URL']
service_url_test = environ['NAMECHEAP_SERVICE_URL_TEST']
api_username = environ['NAMECHEAP_USERNAME']
api_key = environ['NAMECHEAP_API_KEY']
api_key_test = environ['NAMECHEAP_API_KEY_TEST']
client_ip = environ['NAMECHEAP_CLIENT_ID']

# change these to 'is' and 'gay' when the time is right
SLD = 'emilycogsdill'
TLD = 'xyz'

# Stripe
api_secret_prod = environ['STRIPE_SECRET_KEY']

# CREATE FLASK
# +++++++++++++++++++++++

with app.app_context():
    # Flask-WTF requires an enryption key - the string can be anything
    current_app.config['SECRET_KEY'] = 'MLXH243GssUWwKdTWS7FDhdwYF56wPj8'
    
    current_app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    current_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    
    # config for flask-mail protocol
    current_app.config['MAIL_SERVER'] = 'smtp.privateemail.com'
    current_app.config['MAIL_PORT'] = 465
    current_app.config['MAIL_USE_SSL'] = True
    current_app.config['MAIL_USERNAME'] = "gay@is.gay"
    current_app.config['MAIL_PASSWORD'] = environ['GAY_EMAIL_PASSWORD']


# Flask-Bootstrap requires this line
Bootstrap(app)

mail = Mail(app)

engine = create_engine(SQLALCHEMY_DATABASE_URI)

# this variable, db, will be used for all SQLAlchemy commands
db = SQLAlchemy(app)


app.register_blueprint(routes)

application = app # our hosting requires application in passenger_wsgi


# DB OBJECTS
# +++++++++++++++++++++++

class User(db.Model):
    __tablename__ = 'accounts'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String)
    password = db.Column(db.String)
    email = db.Column(db.String)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)

    def __init__(self, username, password, email, first_name, last_name):
        self.username = username
        self.password = password
        self.email = email
        self.first_name = first_name
        self.last_name = last_name

                      
def get_reset_token(username,expires=500):
    return jwt.encode({'reset_password': username,
                       'exp':    time.time() + expires},
                       key=environ['SECRET_KEY_FLASK']
                     )                      

def verify_reset_token(token):
    try:
        username = jwt.decode(token, key=os.getenv('SECRET_KEY_FLASK'))['reset_password']
    except Exception as e:
        print(e)
        return
    return User.query.filter_by(username=username).first()

