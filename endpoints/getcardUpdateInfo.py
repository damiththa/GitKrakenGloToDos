import json
import os

import requests

# auths
from commons.auths.checkSignature import verifySignature

# helpers
from commons.helpers.helperFuncs import is_recurring_task, getRecurringTask, taks_new_dueDate, cardinfo_intoDB as do_intoDB, cardInfo_deleteFromDB as do_deleteFromDB, cardInfo_updateDB as do_updateDB

from datetime import datetime, timedelta
from pytz import timezone # to work with correct timezones

now_datetime = datetime.now(timezone('US/Eastern')) # data/time in the correct timezone

# Glo
BOARD_ID = os.environ['BOARD_ID'] # CHECKME: and see whether this is important to be a environ. varible
COLUMN_ID = os.environ['COLUMN_ID']

# endpoints
POST_CARDUPDATES_ENDPOINT = os.environ['POST_CARDUPDATES_ENDPOINT']

# interested card actions list
card_actions = ['added', 'deleted', 'moved_column']

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
    # print (event)
    
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

        cardId = eventBody['card']['id']
        card_BoradId = eventBody['card']['board_id']
        now_columnId = eventBody['card']['column_id'] if 'column_id' in eventBody['card'] else '1122334455' # column id
        # NOTEME: Making sure there is a value for 'column_id' if not setting up with a bogus column_id. 
        # This is important as webhook fires on every event to card. But we are only interested if the card is moved to predefined column only

        # Next steps depensing on card action
        if cardAction == card_actions[0]: # checking if action is 'added', that means this card is just being added to the board as a new task
            do_intoDB(cardId, card_BoradId, now_columnId)

        elif cardAction == card_actions[1]: # checking if action is 'deleted', that means this card is deleted from this board
            do_deleteFromDB(cardId, card_BoradId)

        elif cardAction == card_actions[2] : # checking if action is 'moved_column' 
            print (BOARD_ID)
            print (COLUMN_ID)

            if now_columnId != COLUMN_ID : # Checking card new column
                do_updateDB(cardId, card_BoradId, now_columnId)

            else: # This is the criteria we are interested in i.e. the 'CLOSED' column

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
