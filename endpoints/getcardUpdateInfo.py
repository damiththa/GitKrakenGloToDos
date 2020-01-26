import json

from commons.auths.checkSignature import verifySignature

def handler(event, context):
    print (event)
    
    event_body = event['body']
    event_headers = event['headers']

    glo_signature = event_headers['x-gk-signature']
    # print (glo_signature)
    
    # verifing headder signatures
    # this is to make sure this payload was sent by GLO
    print (verifySignature(event_body, glo_signature))


    print ('I should see this - POST FUNCTION')
    body = {
        "message": "Go Serverless v1.0! Your function executed successfully! -- POST function",
        "input": event
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response
