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

import json

logging.basicConfig(level=logging.INFO)


# ROUTES
# +++++++++++++++++++++++

@routes.route('/stripeTest')
def stripeTest():
    
    new_events = stripe.getNewStripeEvents()

    
    base_sql = f"""
        INSERT INTO stripe_events
        (stripe_event_id,
        event_type,
        event_datetime_utc_epoch,
        event_datetime_utc,
        event_datetime,
        customer_id,
        amount,
        amount_captured,
        amount_refunded,
        amount_due,
        amount_paid,
        amount_remaining
        )
        VALUES
        """
    
    
    for event in new_events:
    
        #generate the SQL to execute to add this event to the database
        event_sql = stripe.createInsertStatement(event)
        full_sql_for_event = base_sql + event_sql
    
        #run the SQL to add it to the db
        mysql.executeQuery(full_sql_for_event)

    return "great job"    

@routes.route('/getStripeEventIDs')
def getStripeEventIDs():
    
    sql = '''SELECT stripe_event_id FROM stripe_events;'''
    #results = json.dumps(mysql.getQueryResults(sql))
    
    results = mysql.getQueryResults(sql)
    
    #construct a URL from this dict
    list_of_stripe_event_ids=[]
    i=1
    
    for elem in results:
        
        event_id = elem['stripe_event_id']
        list_of_stripe_event_ids.append(event_id)
        
    #TODO:
    
    #get all stripe events
    #remove any event_ids present in list_of_stripe_event_ids
    #create SQL statement inserting new rows
    #ship it
    
    return ','.join(list_of_stripe_event_ids)


@routes.route('/createInvoice')
def createInvoice():
    
    username = session['username']
    
    #get user's Stripe id
    stripe_customer_id = mysql.GetStripeIDFromUsername(username)
    
    stripe.createOneYearInvoice(stripe_customer_id)
    
    return f"Created invoice for customer {stripe_customer_id} ({username})"

#This runs after confirming payment via stripe

@routes.route('/confirmSubscription')
def confirmSubscription():    
    subscriptions_sql = f"INSERT INTO subscriptions (host_id, name, is_active, is_premium) VALUES ({host_id}, '{host_name}', 0, {is_premium});"
    
    start_date = datetime.now()
    end_date = datetime.now() + timedelta(days=364)
    hosts_sql1 = f"UPDATE hosts SET is_active = 1, start_date = {start_date}, end_date = {end_date}, last_updated_at = {start_date} WHERE host_name = '{host_name}';"
    
    #update DNS