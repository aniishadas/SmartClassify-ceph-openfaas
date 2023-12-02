import boto3
import time
import requests
import json

# INPUT_BUCKET = "blankspace-proj2-input"
# OUTPUT_BUCKET = "blankspace-proj2-output"
# AWS_KEY = "AKIAQFDPJDC7MVSOJ4DK"
# AWS_SECRET_KEY = "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"
# REGION = 'us-east-1'

# s3 = boto3.client("s3", aws_access_key_id=AWS_KEY, aws_secret_access_key=AWS_SECRET_KEY,
#                   region_name=REGION)
# openfaas_url = "http://127.0.0.1:8080/function/face-recognition-openfaas-deb"

# if __name__=="__main__":
#     while True:
#         objects = s3.list_objects_v2(Bucket=INPUT_BUCKET)
#         if objects.get('Contents'):
#             for obj in objects['Contents']:
#                 # print(obj)
#                 print(obj['Key'])
#                 data = {'Key':obj['Key']}
#                 data = json.dumps(data)
#                 response = requests.post(url=openfaas_url, data=data)
#                 print(response.status_code)
#                 print(response.text)
#                 s3.delete_object(Bucket=INPUT_BUCKET, Key=obj['Key'])
#         time.sleep(2)


from botocore.config import Config

INPUT_BUCKET = 'ceph-bkt-input-blankspace'
OUTPUT_BUCKET = "ceph-bkt-output-blankspace"
access_key = 'AU18J6SD0PU9YDWK0IHM'
secret_key = '5jbeV6owq1g5ByCRDHH4PfN6IvhRhAMFjYwGgWEU'
endpoint_url = 'http://192.168.49.2:31995'

config = Config(signature_version='s3v4', s3={'addressing_style': 'path'})

rgw_s3_client = boto3.client('s3',
                             endpoint_url=endpoint_url, 
                             aws_access_key_id=access_key, 
                             aws_secret_access_key=secret_key,
                             config=config)
openfaas_url = "http://127.0.0.1:8080/function/face-recognition-openfaas-deb"

if __name__=="__main__":
    start = time.time()
    while True:
        objects = rgw_s3_client.list_objects_v2(Bucket=INPUT_BUCKET)
        if objects.get('Contents'):
            for obj in objects['Contents']:
                # print(obj)
                print(obj['Key'])
                data = {'Key':obj['Key']}
                data = json.dumps(data)
                response = requests.post(url=openfaas_url, data=data)
                print(response.status_code)
                print(response.text)
                rgw_s3_client.delete_object(Bucket=INPUT_BUCKET, Key=obj['Key'])
        else:
            end = time.time()
            print(f"Total time: {end-start}")
            break
        time.sleep(5)
        