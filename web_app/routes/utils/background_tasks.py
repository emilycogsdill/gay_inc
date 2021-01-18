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

import sys
sys.path.append('/home/isgasygd/dev/routes/utils')

from mysql_utils import *
from namecheap_utils import *
from stripe_utils import *



# DATABASE ENGINE
# +++++++++++++++++++++++
engine = createEngine() #from mysql_utils


def updateStripeEvents():
    
    new_events = getNewStripeEvents()

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
        event_sql = createInsertStatement(event)
        full_sql_for_event = base_sql + event_sql
    
        #run the SQL to add it to the db
        executeQuery(full_sql_for_event)


def trackExecutions():
    """
    Keep track of whether this thing is actually running
    """
    
    sql = '''
            INSERT INTO background_task_executions (timestamp) SELECT NOW();
          '''
    executeQuery(sql)

def updateSubscriptionActiveStatus():
    """
    Update the `is_active` flags in the subscriptions table so that it only has one record per host (using most recent end_date)
    
    `active_subscriptions` is a view that returns the subscription id for each valid host_name (having valid start and end datetimes) with the most recent end_date.
    
    This means that if there is an active subscription we want to make inactive, the way to do that is to UPDATE THE END_DATE VALUE (set to NOW()). This means the is_active flag will update to "false" on the next run of this background process.
    """
    
    sql = '''
            UPDATE subscriptions SET is_active = true, last_updated_at = (SELECT DATE_ADD(current_timestamp(), INTERVAL -1 HOUR)) 
            WHERE is_active = false and id in (select id from active_subscriptions);
            
            UPDATE subscriptions SET is_active = false, last_updated_at = (SELECT DATE_ADD(current_timestamp(), INTERVAL -1 HOUR)) 
            WHERE is_active = true and id not in (select id from active_subscriptions);
            
            UPDATE hosts SET is_active = true, last_updated_at = (SELECT DATE_ADD(current_timestamp(), INTERVAL -1 HOUR))
            WHERE is_active = false and host_name in (select host_name from active_subscriptions);
            
            UPDATE hosts SET is_active = false, last_updated_at = (SELECT DATE_ADD(current_timestamp(), INTERVAL -1 HOUR))
            WHERE is_active = true and host_name not in (select host_name from active_subscriptions);
          '''
    executeQuery(sql)

def updateDNS():    
    """
    update DNS to reflect current state of the subscriptions table
    (this allows us to have users test new subdomains by creating a new subscription record when they register an auto-approved domain, but set the end_date timestamp to be only a half hour after it started)
    """
    url = setHostsURLFromDb()
    resp = requests.post(url)
    
    timestamp = datetime.now()
