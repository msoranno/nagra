#---------------------------
#---------------------------
# - This function interactn with the omdb api and create json files on a bucket. This function react to a http-GET event.
# - The general idea is to create a interface to grab movies info from omdb platform (need to be register first).
# - If the movie is found a json file will be created in the configure bucket specified in serverless.yml.
# - In the samples below the json files will be: rocky.json and top+gun.json
# - At this point the only way to search is by tittle /?t=
# 
# e.g :
# https://url-endpoint/playme?movie=rocky
# https://url-endpoint/playme?movie=top+gun
# 
#
# Serverless cheat:
# Print output:
# sls logs -f requesterFunc -t
# Redeploy only this function:
# sls deploy function -f requesterFunc
#---------------------------
#---------------------------


#-------
# serverless.yml contains  zip:true
# uncompress dependencies compressed before
# pulgin: serverless-python-requirements
#------
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
    try:
        findMovie = event["queryStringParameters"]['movie'].replace(" ", "+")
    except Exception as e:
        #print(e)
        txt='Bad formed. excpected something like /playme?movie=top+gun '
        print(txt)
        response = {
            "statusCode": 200,
            "body": txt
        }
        return response
        raise e
        
    print('Movie to find:', findMovie)
    omdbApiKey = os.environ['OMDB_KEY'] 
    bucket = os.environ['BUCKET_NAME'] 
    jsonFolder = os.environ['JSON_BUCKET_KEY']
    json_file = jsonFolder + "/" + findMovie + ".json"
    url = os.environ['OMDB_URL'] +"/?t=" + findMovie + "&apikey=" + omdbApiKey
    respuesta = requests.get(url)
    movie_dict = json.loads(respuesta.text)
    #change dict to json
    json_response = json.dumps(movie_dict)
    if 'Error' in movie_dict:
        print("Error: Movie ", findMovie, " not found")
    else:
        # read key values from dic
        #for key, value in movie_dict.items():
        #    print(key, value)
        print(json_response) 
        #-- create the buffer
        s3.put_object(Bucket=bucket, Key=json_file, Body=json_response)

    response = {
        "statusCode": 200,
        "body": json.dumps(json_response)
    }
    return response


