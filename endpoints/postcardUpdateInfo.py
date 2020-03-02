import json
import os

import requests

# Glo
BOARD_ID = os.environ['BOARD_ID']
COLUMN_ID = os.environ['COLUMN_ID']

# endpoint
POST_CARDUPDATES_ENDPOINT = os.environ['POST_CARDUPDATES_ENDPOINT']

def handler(event, context):
    print ('------------------------')
    print (event)

    cardBody = {
        "name": "NEW NAME - Testing card - NEW TEST",
        "position": 0,
        "description": {"text":"added this desc\n\nDesc 2\nDesc 3"},
        "column_id": "5e29201b70ae270011d1e5b5",
        "labels": [{"name":"recuring task - MONTHLY","id":"5e1b3155553d4500116e11da"}],
        "due_date": "2020-07-25"
    }

    url = 'https://gloapi.gitkraken.com/v1/glo/boards/5e1b2b8a553d4500116e117d/cards/5e483eb80e8c720011032f21'
    headers = {
        'Content-Type' : 'application/json'
    }
    payload = {
        "messageToPublish" : cardBody
    }

    print (url)
    # res = requests.post(url, headers=headers, data=json.dumps(payload))
    # print (res.status_code)
    # print (res.content)

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
