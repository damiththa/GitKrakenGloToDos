import json
import os

import requests

# Glo
BOARD_ID = os.environ['BOARD_ID']
COLUMN_ID = os.environ['COLUMN_ID']

# endpoint
POST_CARDUPDATES_ENDPOINT = os.environ['POST_CARDUPDATES_ENDPOINT']

# Glo webhook
GLO_API_AUTH_TOKEN = os.environ['GLO_API_AUTH_TOKEN']

def handler(event, context):
    # print (event)

    event_body = event['body']
    # print (event_body)
    
    eventBody = json.loads(event_body) # converting string into a pythong dict. object
    cardInfo = eventBody['cardInfoToPost']
    # print (cardInfo) 

    payload = {
        "position": cardInfo['card_position'],
        "column_id": cardInfo['columnID'],
        "due_date": cardInfo['cardDueDate']
    }
    
    url = 'https://gloapi.gitkraken.com/v1/glo/boards/' + cardInfo['boardID'] + '/cards/' + cardInfo['cardID']
    headers = {
        'Content-Type' : 'application/json',
        'Authorization' : GLO_API_AUTH_TOKEN
    }

    # print (url)
    res = requests.post(url, headers=headers, data=json.dumps(payload))
    print (res.status_code)
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
