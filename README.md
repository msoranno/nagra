# From json to csv project (Serverless + lambda + S3 bucket)

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
### Serverless framework
- Install nodeJs v6.X
- Install npm
- with npm install serverless
  sudo npm install -g serverless
  - Now you can call serverless cli by doing
    - serverless or simple sls
- Give aws credential to your serverless 
  - sls config credentials --provider aws --key YOURKEY --secret YOURSECRET
- Clone this repo
  - git clone https://github.com/msoranno/nagra.git
- Go into nagra directory
  - create the environment file called serverless.env.yml, and put this content (modifiy the content)
    ```
    dev:
    KEY_OMDB: 'YOUR-OMDB-KEY-HERE'
    BUCKET_NAME: nagra-omdb
    JSON_BUCKET_KEY: jsonFolder
    CVS_BUCKET_KEY: csvHere
    OMDB_URL: 'http://www.omdbapi.com'
    ```
    - where:
      - KEY_OMDB: is the key to access to the omdb api, you received this after register to the service.
      - BUCKET_NAME: The bucket name to work with
      - JSON_BUCKET_KEY: place to the json files
      - CVS_BUCKET_KEY: place to the csv files
      - OMDB_URL: pretty clear.
   - At this point your nagra directory should have this content:
     ```
      README.md
      handler
      .gitignore
      some_notes.txt
      serverless.yml
      requester
      node_modules
      .git
      serverless.env.yml
     ```
   - TO BE CONTINUE.....


  
