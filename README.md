# From json to csv project

## What is this ?
- The general idea is to convert .json to .csv files working on s3 bucket.
- Everything will be done from Lamda functions using python 3.6

## Platforms and technologies involved
- AWS Lambda Functions
- AWS S3
- Serverless framework
  - Plugins
    - serverless-python-individually
    - serverless-s3-remover (WARNING: should be disabled in servless.yml on PROD)
- Python 3.6
  - pip libraries
    - Pandas
    - Requests
- OMDB Api
  - http://www.omdbapi.com/
  

## How it works ?
Two lambda functions will be created: requester and handler.

- requester
  This function interactn with the omdb api and create json files on a bucket. This function react to a http-GET event.
  The general idea is to create a interface to grab movies info from omdb platform (need to be register first).
  If the movie is found a json file will be created in the configure bucket specified in serverless.yml.

  In the samples below the json files will be: rocky.json and top+gun.json
  At this point the only way to search is by tittle /?t=
  e.g :
  https://url-endpoint/playme?movie=rocky
  https://url-endpoint/playme?movie=top+gun

- handler
  This function react over a S3PutObject event and create another object in csv format in a different folder same bucket.
  As configured in serverless.yml this function is triggered only when a .json file is created in a specific folder.
  e.g Input:
  rocky.json
  e.g Output(dateTime includded):
  rocky.2017-10-2919.00.51.240533.csv


## How to use it ?
