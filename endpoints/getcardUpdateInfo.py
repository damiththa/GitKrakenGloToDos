import json
import os

from commons.auths.checkSignature import verifySignature
from commons.helpers.helperFuncs import is_recurring_task, getRecurringTask

BOARD_ID = os.environ['BOARD_ID']
COLUMN_ID = os.environ['COLUMN_ID']

# interested card actions list
card_actions = ['moved_column']

def handler(event, context):
    # print (event)
    # HARDCODED: for testing
    event = {'resource': '/getCardUpdates', 'path': '/getCardUpdates', 'httpMethod': 'POST', 'headers': {'Accept': 'application/json', 'client': '', 'CloudFront-Forwarded-Proto': 'https',
 'CloudFront-Is-Desktop-Viewer': 'true', 'CloudFront-Is-Mobile-Viewer': 'false', 'CloudFront-Is-SmartTV-Viewer': 'false', 'CloudFront-Is-Tablet-Viewer': 'false', 'CloudFront-Viewer-Country': 'US', 'content-type': 'application/json', 'Host': 'z7jpehbxgl.execute-api.us-east-2.amazonaws.com', 'User-Agent': 'gk-webhooks', 'Via': '1.1 05a90e634e0872685ad69ee9a4e0eba5.cloudfront.net (CloudFront)', 'X-Amz-Cf-Id': 'Afb9dkZR75jxsbB-fo5QUVPF-B1j9sKA-Lk3ppjXV8ulFlrjr8_Y0Q==', 'X-Amzn-Trace-Id': 'Root=1-5e484b47-780288fc9e01c35a93264d51', 'X-Forwarded-For': '34.235.241.195, 70.132.60.67', 'X-Forwarded-Port': '443', 'X-Forwarded-Proto': 'https', 'x-gk-event': 'cards', 'x-gk-signature': 'sha1=d9ae31fe4a2e18429d53633df8fc39e3e0b7d486'}, 'multiValueHeaders': {'Accept': ['application/json'], 'client': [''], 'CloudFront-Forwarded-Proto': ['https'], 'CloudFront-Is-Desktop-Viewer': ['true'], 'CloudFront-Is-Mobile-Viewer': ['false'], 'CloudFront-Is-SmartTV-Viewer': ['false'], 'CloudFront-Is-Tablet-Viewer': ['false'], 'CloudFront-Viewer-Country': ['US'], 'content-type': ['application/json'], 'Host': ['z7jpehbxgl.execute-api.us-east-2.amazonaws.com'], 'User-Agent': ['gk-webhooks'], 'Via': ['1.1 05a90e634e0872685ad69ee9a4e0eba5.cloudfront.net (CloudFront)'], 'X-Amz-Cf-Id': ['Afb9dkZR75jxsbB-fo5QUVPF-B1j9sKA-Lk3ppjXV8ulFlrjr8_Y0Q=='], 'X-Amzn-Trace-Id': ['Root=1-5e484b47-780288fc9e01c35a93264d51'], 'X-Forwarded-For': ['34.235.241.195, 70.132.60.67'], 'X-Forwarded-Port': ['443'], 'X-Forwarded-Proto': ['https'], 'x-gk-event': ['cards'], 'x-gk-signature': ['sha1=d9ae31fe4a2e18429d53633df8fc39e3e0b7d486']}, 'queryStringParameters': None, 'multiValueQueryStringParameters': None, 'pathParameters': None, 'stageVariables': None, 'requestContext': {'resourceId': 'netxbp', 'resourcePath': '/getCardUpdates', 'httpMethod': 'POST', 'extendedRequestId': 'H9CzKH4qCYcFweA=', 'requestTime': '15/Feb/2020:19:49:27 +0000', 'path': '/prod/getCardUpdates', 'accountId': '877428826965', 'protocol': 'HTTP/1.1', 'stage': 'prod', 'domainPrefix': 'z7jpehbxgl', 'requestTimeEpoch': 1581796167331, 'requestId': '5bfc437d-fd32-471f-b10c-98d22eece256', 'identity': {'cognitoIdentityPoolId': None, 'accountId': None, 'cognitoIdentityId': None, 'caller': None, 'sourceIp': '34.235.241.195', 'principalOrgId': None, 'accessKey': None, 'cognitoAuthenticationType': None, 'cognitoAuthenticationProvider': None, 'userArn': None, 'userAgent': 'gk-webhooks', 'user': None}, 'domainName': 'z7jpehbxgl.execute-api.us-east-2.amazonaws.com', 'apiId': 'z7jpehbxgl'}, 'body': '{"action":"moved_column","board":{"id":"5e1b2b8a553d4500116e117d","name":"ToDos"},"card":{"id":"5e483eb80e8c720011032f21","name":"Testing card","created_date":"2020-02-15T18:55:52.058Z","board_id":"5e1b2b8a553d4500116e117d","column_id":"5e29201b70ae270011d1e5b5","due_date":"2020-02-27T05:00:00.000Z","description":{"text":"added this desc\\n\\nDesc 2\\nDesc 3"},"labels":[{"name":"recuring task - MONTHLY","id":"5e1b3155553d4500116e11da"}],"assignees":[],"completed_task_count":0,"total_task_count":0,"attachment_count":0,"comment_count":1,"created_by":{"id":"65f0a2cf-194f-42a3-b280-16193a7e5bad"},"position":0},"sender":{"name":"Madushan D. Memmendarachchi","id":"65f0a2cf-194f-42a3-b280-16193a7e5bad","username":"damiththa"},"sequence":40}', 'isBase64Encoded': False}
    
    event_body = event['body']
    event_headers = event['headers']

    glo_signature = event_headers['x-gk-signature']
    # print (glo_signature)
    
    # verifing header signatures
    # this is to make sure this payload was sent by GLO
    if verifySignature(event_body, glo_signature):
        # We PASSED and verified. Good to go
        
        # print (event_body)
        # # HARDCODED: for testing
        # event_body = {"action":"moved_column","board":{"id":"5e1b2b8a553d4500116e117d","name":"ToDos"},"card":{"id":"5e483eb80e8c720011032f21","name":"Testing card","created_date":"2020-02-15T18:55:52.058Z","board_id":"5e1b2b8a553d4500116e117d","column_id":"5e28527c1d0b4a00107c3884","due_date":"2020-02-27T05:00:00.000Z","description":{"text":"added this desc\n\nDesc 2\nDesc 3"},"labels":[{"name":"recuring task - MONTHLY","id":"5e1b3155553d4500116e11da"}],"assignees":[],"completed_task_count":0,"total_task_count":0,"attachment_count":0,"comment_count":1,"created_by":{"id":"65f0a2cf-194f-42a3-b280-16193a7e5bad"},"position":0},"sender":{"name":"Madushan D. Memmendarachchi","id":"65f0a2cf-194f-42a3-b280-16193a7e5bad","username":"damiththa"},"sequence":41}

        eventBody = json.loads(event_body) # converting string into a pythong dict. object

        # print (eventBody['action'])
        # print (eventBody['card'])
        # print (eventBody['card']['column_id'])

        cardAction = eventBody['action'] # card action i.e. what triggered this call
        now_columnId = eventBody['card']['column_id'] # column ID i.e. where this card is now
        labels_lst = eventBody['card']['labels'] # List of labels in the body

        # checking if action is 'moved_column' AND moved to the 'CLOSED' column
        if cardAction == card_actions[0] and now_columnId == COLUMN_ID :  # This is the criteria we are interested in
            print (BOARD_ID)
            print (COLUMN_ID)

            # CHECKME: test how this will work on an actual list of recurring task list
            if is_recurring_task(labels_lst): # checking if this is a recurring task

                print (getRecurringTask(labels_lst))

                

        # TODO: Check is there is a 'due date' node is always there even when a date is not set

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
