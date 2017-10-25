import json
import urllib.parse
import boto3
import os
import datetime
import io


print('Loading function')
s3 = boto3.client('s3')

def omdbrequest(event, context):
    #print("Received event: " + json.dumps(event, indent=2))
    body = {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "input": event
    }

    try:
        findMovie = event["queryStringParameters"]['movie']
        print('Movie to find:', findMovie)
    except Exception as e:
        print(e)
        print('Bad formed. excpected something like /playme?movie=maraco+volador ')
        raise e
    return body


# event['pathParameters']['param1']
# event['requestContext']['identity']['userAgent']
# event['requestContext']['identity']['sourceIP']