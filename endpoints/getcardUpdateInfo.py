import json


def handler(event, context):
    print (event)
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
