import json, requests
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

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    try:
        findMovie = event["queryStringParameters"]['movie']
        print('Movie to find:', findMovie)
        omdbApiKey="ecd349ff"
        url = "http://www.omdbapi.com/?t=" + findMovie + "&apikey=" + omdbApiKey
        response = requests.get(url)
        movie_dict = json.loads(response.text)
        print(movie_dict)
    except Exception as e:
        print(e)
        print('Bad formed. excpected something like /playme?movie=maraco+volador ')
        raise e
    return response


# event['pathParameters']['param1']
# event['requestContext']['identity']['userAgent']
# event['requestContext']['identity']['sourceIP']