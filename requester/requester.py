# try:
#   import unzip_requirements
# except ImportError:
#   pass

import json
import requests
import boto3
import os
import datetime
import io


print('Loading function')
s3 = boto3.client('s3')

def omdbrequest(event, context):
    #print("Received event: " + json.dumps(event, indent=2))
    # body = {
    #     "message": "Go Serverless v1.0! Your function executed successfully!",
    #     "input": event
    # }


    try:
        findMovie = event["queryStringParameters"]['movie'].replace(" ", "+")
        print('Movie to find:', findMovie)
        omdbApiKey="ecd349ff"
        url = "http://www.omdbapi.com/?t=" + findMovie + "&apikey=" + omdbApiKey
        respuesta = requests.get(url)
        movie_dict = json.loads(respuesta.text)
        #change dict to json
        json_response = json.dumps(movie_dict)
        print(json_response)
        #-- create the buffer
        bucket = "nagra-omdb"
        json_file = "jsonFolder/" + findMovie + ".json"
        s3.put_object(Bucket=bucket, Key=json_file, Body=json_response)

    except Exception as e:
        print(e)
        print('Bad formed. excpected something like /playme?movie=maraco+volador ')
        raise e

    response = {
        "statusCode": 200,
        "body": json.dumps(json_response)
    }
    return response


# event['pathParameters']['param1']
# event['requestContext']['identity']['userAgent']
# event['requestContext']['identity']['sourceIP']