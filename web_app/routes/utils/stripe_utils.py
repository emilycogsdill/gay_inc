# get the data to add to the database
import stripe
from os import environ
import json
from datetime import datetime
import pytz

# authentication
api_secret_prod = environ['STRIPE_SECRET_KEY']

stripe.api_key = api_secret_prod

def createCustomer(email, username, *first_name, *last_name):

    '''
    When a user registers on the site, create a Stripe customer record for them.
    Function creates the Stripe customer and returns the customer_id.
    '''
    
    response = stripe.Customer.create(
       email = email
      #,name = username
      ,name = first_name + ' ' + last_name
      ,description = username
    )
    
    #extract the Stripe customer_id from the new record
    cust_json_dump = json.dumps(response)
    cust_json = json.loads(cust_json_dump)
    customer_id = cust_json['id']
    
    return customer_id


def getChargeSuccessEvents():

    #get "Charge Succeeded" events from Stripe
    events=stripe.Event.list(type='charge.succeeded') #this also takes a limit parameter - maybe someday we will have enough business for that to be necessary

    #dump the response object into a json
    json_data = json.dumps(events.__dict__['_previous'])
    json_object = json.loads(json_data)
    
    events = json_object['data']
    
    events_data=[]
    
    for event in events:
        if event['object']=='event':
    
            event_data={}
            event_data['event_id']=event['id']
            event_data['event_type']=event['type']
            #--TIMESTAMP----------
            createdate_epoch = event['created']
            event_data['createdate_epoch']=createdate_epoch
            # get time in tz
            tz_utc = pytz.timezone('UTC')
            event_data['createdate_timestamp_utc'] = datetime.fromtimestamp(createdate_epoch, tz_utc).strftime('%Y-%m-%d %H:%M:%S')
            # get time in Eastern
            tz = pytz.timezone('America/New_York')
            event_data['createdate_timestamp'] = datetime.fromtimestamp(createdate_epoch, tz).strftime('%Y-%m-%d %H:%M:%S')
            
            event_data['customer_id'] = event['data']['object']['customer']
            event_data['amount'] = event['data']['object']['amount']
            event_data['amount_captured'] = event['data']['object']['amount_captured']
            event_data['amount_refunded'] = event['data']['object']['amount_refunded']
            
            events_data.append(event_data)
            
    return events_data

def initiateMonthly(customer_id):
    #initiate a monthly subdomain invoice. This sends an invoice for a one-time payment and begins a monthly subscription for that customer
    
    
    stripe.InvoiceItem.create(
       price='price_1HvQfgGun3mcXhIzqPb1QzmX' # $1 one-time
      ,customer=customer_id
    )

    invoice = stripe.Invoice.create(
      customer='cus_IWTUl5tWJsriRv',
      collection_method='send_invoice',
      days_until_due=7,
      description='This confirms your use of the subdomain for the 30 day period starting from successful payment of this invoice. By paying this invoice you are agreeing to the following Terms of Use: https://tinyurl.com/yxco5c5u'
    )
    
    subscription = stripe.Subscription.create(
      customer=customer,
      items=[{'price': 'price_1Hqix8Gun3mcXhIzEvMZw0ao'}],
      collection_method='send_invoice',
      days_until_due=7,
    )
    
    invoice.send_invoice()