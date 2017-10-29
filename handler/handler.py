#---------------------------
#---------------------------
# - Has requested this function react over a S3PutObject event and create another object in csv format.
# - Uses Pandas Library
# - As configured in serverless.yml this function is triggered only when a .json file is created in a specific folder.
# - e.g Input:
#   rocky.json
# - e.g Output(dateTime includded):
#   rocky.2017-10-2919.00.51.240533.csv
#
# Serverless cheat:
# Print output:
# sls logs -f handlerFunc -t
# Redeploy only this function:
# sls deploy function -f handlerFunc
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
import urllib.parse
import boto3
import os
import lib.pandas as pd
import datetime
import io


print('Loading function')
s3 = boto3.client('s3')

def get_NOW():
    return str(datetime.datetime.now()).replace(" ", "").replace(":",".")

def jsonToCsv(event, context):
    #print("Received event: " + json.dumps(event, indent=2))

    #-- get bucket and key from event
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')

    #getting a valid filename key for cvs
    csv_s3_store = os.environ['CVS_BUCKET_KEY'] #defined in serverless.yml
    just_file = key.split('/')[1]
    just_file_noExt = just_file.split('.json')[0]
    csv_file = just_file_noExt + '.' + get_NOW() + '.csv'
    csv_file_s3 = csv_s3_store + '/' + csv_file
    #-----
    # debug
    # print("Key json: ", key)
    # print("File json: ", just_file)
    # print("File json no ext: ", just_file_noExt)
    # print('download_path: ' + download_path)
    # print('csv_file: ' + csv_file)
    # print('csv_file_s3: ' + csv_file_s3)
    #------

    #---
    # Read the body content and create the pandas dataframe
    #---
    try:
        response = s3.get_object(Bucket=bucket, Key=key)
    except Exception as e:
        print(e)
        print('Error reading object on bucket ', bucket , ' key ', key)
        raise e
    dataframe = pd.read_json(response['Body'].read())
    #print(dataframe)
    
    #-- create the buffer
    csv_buffer = io.StringIO()

    #-- 
    # pandas df to_csv
    # encoding default  ‘utf-8’ on Python 3
    #--
    dataframe.to_csv(csv_buffer, index=False)

    #--
    # with string buffer in memory we write the objetc
    #--
    try:
        s3.put_object(Bucket=bucket, Key=csv_file_s3, Body=csv_buffer.getvalue())
    except Exception as e:
        print(e)
        print('Error putting object on bucket ', bucket , ' key ', key)
        raise e



    

