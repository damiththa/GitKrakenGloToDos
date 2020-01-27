import json

from commons.auths.checkSignature import verifySignature

def handler(event, context):
    # print (event)
    
    event_body = event['body']
    event_headers = event['headers']

    glo_signature = event_headers['x-gk-signature']
    # print (glo_signature)
    
    # verifing headder signatures
    # this is to make sure this payload was sent by GLO
    if verifySignature(event_body, glo_signature):
        print ('We are good to continue')
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
