import json
import os

import requests

# auths
from commons.auths.checkSignature import verifySignature

# helpers
from commons.helpers.helperFuncs import is_recurring_task, getRecurringTask, taks_new_dueDate

from datetime import datetime, timedelta
from pytz import timezone # to work with correct timezones

now_datetime = datetime.now(timezone('US/Eastern')) # data/time in the correct timezone

# Glo
BOARD_ID = os.environ['BOARD_ID']
COLUMN_ID = os.environ['COLUMN_ID']

# endpoints
POST_CARDUPDATES_ENDPOINT = os.environ['POST_CARDUPDATES_ENDPOINT']

# interested card actions list
card_actions = ['moved_column']

# posting to fusionqc activity logger lambda
def XX(eBody):

    url = POST_CARDUPDATES_ENDPOINT
    headers = {
        'Content-Type' : 'application/json'
    }
    payload = {
        "messageToPublish" : eBody
    }

    res = requests.post(url, headers=headers, data=json.dumps(payload))
    print (res.status_code)

def handler(event, context):
    print (event)
    
    event_body = event['body']
    event_headers = event['headers']

    glo_signature = event_headers['x-gk-signature']
    # print (glo_signature)
    
    # verifing header signatures
    # this is to make sure this payload was sent by GLO
    if verifySignature(event_body, glo_signature):
        # We PASSED and verified. Good to go
        
        print (event_body)

        eventBody = json.loads(event_body) # converting string into a pythong dict. object

        # print (eventBody['action'])
        # print (eventBody['card'])
        # print (eventBody['card']['column_id'])

        cardAction = eventBody['action'] # card action i.e. what triggered this call

        now_columnId = eventBody['card']['column_id'] if 'column_id' in eventBody['card'] else '1122334455' # column id
        # NOTEME: Making sure there is a value for 'column_id' if not setting up with a bogus column_id
        # This is important as webhook fires on every event to card but we are here only interested if the card is moved to predefined column only

        # checking if action is 'moved_column' AND moved to the 'CLOSED' column
        if cardAction == card_actions[0] and now_columnId == COLUMN_ID :  # This is the criteria we are interested in
            print (BOARD_ID)
            print (COLUMN_ID)

            labels_lst = eventBody['card']['labels'] # List of labels in the body

            # checking if this is a recurring task
            if is_recurring_task(labels_lst):

                print (getRecurringTask(labels_lst))
                recurring_task_tup = getRecurringTask(labels_lst)
                recurring_task_val = recurring_task_tup[0] # getting the first value of returned tuple Ex. --> (1, 'recurring - DAILY')

                # Finsing Task NEW due date accordingly
                if 'due_date' in eventBody['card']: # checking if 'due_date' key in json object, which is a python dict now
                    task_dueDate = eventBody['card']['due_date'] # due date in json which is a string
                    task_dueDate = datetime.fromisoformat(task_dueDate[:-1]) # getting it is python datetime type
                    # NOTEME: to get Gitkraken Glo date rounding correct, substracting a day
                    task_dueDate = task_dueDate - timedelta(days=1) 
                else:
                    # Due date not set, i.e. not in the json therefore setting task original due date to TODAY
                    task_dueDate = now_datetime 

                print (task_dueDate)

                print (taks_new_dueDate(task_dueDate, recurring_task_val))

                print (event_body)

                # THIS IS GOOD
                # XX(event_body)

                #TODO: now that we there is a task that is found, This should be done on a seperate function
                    # See either we can edit the exsisting card (preferred)
                    # If not need to re-create the card with all the info

                
        # TODO: 
        # Also need to get any reactions, comments etc. included in the card as those are not in the card move JSON

    else:
        print ('AUTH. SIGNATURE FAILED!')

    #TODO: this needs to be more meaningful
    # aws lambda return response
    body = {
        "come_back_to_me": 'COME BACK TO ME'
    }
    response = {
        "statusCode": 200, # passing back status 200
        "body": json.dumps(body)
    }
    return response
