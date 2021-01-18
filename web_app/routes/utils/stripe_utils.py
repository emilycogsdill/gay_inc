# get the data to add to the database
import stripe
from os import environ
import json
from datetime import datetime
import pytz

import sys
sys.path.append('/home/isgasygd/dev/routes/utils')

from mysql_utils import *

# authentication
api_secret_prod = environ['STRIPE_SECRET_KEY']

stripe.api_key = api_secret_prod


def getStripeEventIDs():
    '''
    returns list of event IDs already present in MySQL database
    '''
    
    sql = "SELECT stripe_event_id FROM stripe_events;"
    
    results = getQueryResults(sql)
    
    #construct a URL from this dict
    list_of_stripe_event_ids=[]
    i=1
    
    for elem in results:
        
        event_id = elem['stripe_event_id']
        list_of_stripe_event_ids.append(event_id)

    return list_of_stripe_event_ids

def createCustomer(email, username):

    '''
    When a user registers on the site, create a Stripe customer record for them.
    Function creates the Stripe customer and returns the customer_id.
    '''
    
    response = stripe.Customer.create(
       email = email
      ,name = username
      #,name = first_name + ' ' + last_name
      ,description = username
    )
    
    #extract the Stripe customer_id from the new record
    cust_json_dump = json.dumps(response)
    cust_json = json.loads(cust_json_dump)
    customer_id = cust_json['id']
    
    return customer_id



def createOneYearInvoice(customer_id):
    #initiate a monthly subdomain invoice. This sends an invoice for a one-time payment and begins a monthly subscription for that customer
    
    stripe.InvoiceItem.create(
       price='price_1HvQYjGun3mcXhIzyQWn2XaV'
      ,customer=customer_id
    )

    invoice = stripe.Invoice.create(
      customer=customer_id,
      collection_method='send_invoice',
      days_until_due=1,
      description='This confirms your use of the subdomain for the 364 day period starting from successful payment of this invoice. \nYou will receive another invoice next year that you may pay if you wish to continue your subdomain. \n By paying this invoice you are agreeing to the following Terms of Use: https://tinyurl.com/yxco5c5u'
    )
    
    invoice.send_invoice()   
    
def createAnnualSubscription(customer_id):
    stripe.Subscription.create(
          customer='cus_IkR19D09w3YKcQ',
          items=[{'price': 'price_1I9E1ZGun3mcXhIzHvl15eG5'}],
          collection_method='send_invoice',
          days_until_due=1
        )
    
    
'''Use this to update MySQL table with all Stripe events'''    
def tryExcept(event,field_name):
    '''
    returns a value for a field in a Stripe event, or None if not available
    '''
    try:
        if 'cus' in event['data']['object']['id'] and field_name=='customer':
            try:
                value = event['data']['object']['id'] #this is where customer_id lives for "customer" event types
            except KeyError:
                value = None 
        else:
            value = None
    except:
        try:
            value = event['data']['object'][field_name]
        except KeyError:
            value = None
    
    return value

def fillStripeEventData(event, target_dict, field_name_list):
    '''
    populates event data (using try/except logic) for all fields
    '''
    field_values = {}
    for name in field_name_list:
        target_dict[name] = tryExcept(event,name)
    return target_dict

def getNewStripeEvents():
    '''
    returns a list of dicts where each dict item contains information about a Stripe event
    '''
    
    events_list = []
    all_stripe_event_ids = []
    i=0
    
    #cPanel hosting is janky
    stripe.max_network_retries = 10
    
    events = stripe.Event.list()
    for event in events.auto_paging_iter():
        i+=1
        if event['object']=='event':
            
            event_json = json.loads(json.dumps(event))
            
            all_stripe_event_ids.append(event_json['id'])
            event_data={}
            event_data['stripe_event_id']=event_json['id']
            event_data['event_type']=event_json['type']
            
            ##--TIMESTAMP----------
            createdate_epoch = event['created']
            event_data['event_datetime_utc_epoch']=createdate_epoch
            # get time in tz
            tz_utc = pytz.timezone('UTC')
            event_data['event_datetime_utc'] = datetime.fromtimestamp(createdate_epoch, tz_utc).strftime('%Y-%m-%d %H:%M:%S')
            # get time in Central
            tz = pytz.timezone('America/Chicago')
            event_data['event_datetime'] = datetime.fromtimestamp(createdate_epoch, tz).strftime('%Y-%m-%d %H:%M:%S')
            
           #--CUSTOMER ID & AMOUNTS----------

            field_name_list = ['customer','amount_due','amount_paid','amount_remaining','amount','amount_captured','amount_refunded']            
            event_data = fillStripeEventData(event, event_data, field_name_list)
                
            events_list.append(event_data)
    
    #filter out any that are already in the database
    existing_event_ids = getStripeEventIDs()
    
    event_ids_to_push_to_db = [event_id for event_id in all_stripe_event_ids if event_id not in existing_event_ids]

    event_info_to_push_to_db = [event for event in events_list if event['stripe_event_id'] in event_ids_to_push_to_db]
    
    return event_info_to_push_to_db


def coalesceNone(event,field):
    if not event[field]:
        return 'NULL'
    elif 'amount' in field:
        return f"{event[field]}"
    else:
        return f"\'{event[field]}\'"

def createInsertStatement(event):
    '''
    Returns the INSERT statement used to add a single event to the database
    '''
    
    stripe_event_id = event['stripe_event_id']
    event_type = event['event_type']
    event_datetime_utc_epoch = event['event_datetime_utc_epoch']
    event_datetime_utc = event['event_datetime_utc']
    event_datetime = event['event_datetime']
    
    event_sql = f"""
    ('{stripe_event_id}',
     '{event_type}',
      {event_datetime_utc_epoch},
      CAST('{event_datetime_utc}' as DATETIME),
      CAST('{event_datetime}' as DATETIME),
      {coalesceNone(event,'customer')},
      {coalesceNone(event,'amount')},
      {coalesceNone(event,'amount_captured')},
      {coalesceNone(event,'amount_refunded')},
      {coalesceNone(event,'amount_due')},
      {coalesceNone(event,'amount_paid')},
      {coalesceNone(event,'amount_remaining')}
      )
    """
        
    return event_sql