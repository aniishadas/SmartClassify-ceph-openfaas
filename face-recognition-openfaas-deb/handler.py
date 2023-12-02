# def handle(event, context):
#     return {
#         "statusCode": 200,
#         "body": "Hello from OpenFaaS!"
#     }

# def handle(event, context):
#     return {
#         "statusCode": 200,
#         "body": "Hello from OpenFaaS!"
#     }

import boto3
import face_recognition
from urllib.parse import unquote_plus
import pickle
import os
import json
import sys
from botocore.config import Config

access_key = 'AU18J6SD0PU9YDWK0IHM'
secret_key = '5jbeV6owq1g5ByCRDHH4PfN6IvhRhAMFjYwGgWEU'
endpoint_url = 'http://192.168.49.2:31995'
bucket_name1 = 'ceph-bkt-input-blankspace'
bucket_name2 = 'ceph-bkt-output-blankspace'

config = Config(signature_version='s3v4', s3={'addressing_style': 'path'})

INPUT_BUCKET = 'ceph-bkt-input-blankspace'
OUTPUT_BUCKET = 'ceph-bkt-output-blankspace'
DYNAMO_TABLE_NAME = "blankSpace-student-data"
AWS_KEY = "AKIAQFDPJDC7MVSOJ4DK"
AWS_SECRET_KEY = "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"
REGION = 'us-east-1'


def download_video(s3_client, video_key, local_path):
    s3_client.download_file(INPUT_BUCKET, video_key, local_path)


def extract_first_frame_from_video(video_path, image_path):
    command = f"ffmpeg -loglevel quiet -i {video_path} -frames:v 1 -r 1 {image_path}"
    os.system(command=command)


def get_face_rec_result(image_path, encodings_file):
    image_encodings = face_recognition.face_encodings(face_recognition.load_image_file(image_path))[0]
    encoded_file_data = open_encoding(encodings_file)
    face_encodings = encoded_file_data['encoding']

    for i, encoding in enumerate(face_encodings):
        if face_recognition.compare_faces([image_encodings], encoding)[0]:
            return encoded_file_data['name'][i]


def get_student_details(dynamo_client, name):
    response = dynamo_client.get_item(TableName=DYNAMO_TABLE_NAME, Key={'name': {'S': name}})
    return response


def save_results_to_s3(s3_client, filename, details):
    csv_record = f"{details['Item']['name']['S']},{details['Item']['major']['S']},{details['Item']['year']['S']}"
    s3_client.put_object(Key=f'{filename}.csv', Bucket=OUTPUT_BUCKET, Body=csv_record)


# Function to read the 'encoding' file
def open_encoding(filename):
    file = open(filename, "rb")
    data = pickle.load(file)
    file.close()
    return data


def handle(event, context):
    #s3_client = boto3.client('s3', aws_access_key_id=AWS_KEY, aws_secret_access_key=AWS_SECRET_KEY, region_name=REGION)
    rgw_s3_client = boto3.client('s3', endpoint_url=endpoint_url, aws_access_key_id=access_key, 
    aws_secret_access_key=secret_key, config=config)
    dynamo_client = boto3.client('dynamodb', aws_access_key_id=AWS_KEY, aws_secret_access_key=AWS_SECRET_KEY, region_name=REGION)

    # Face recognition handler is called
    # sys.stderr.write(f"event: {event.body}")
    # video_key = unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    sys.stderr.write(f"event: {json.loads(event.body)}")
    video_key = json.loads(event.body)['Key']
    sys.stderr.write(f"video key: {video_key}")
    video_name = os.path.basename(video_key)
    video_path_on_disk = f"/tmp/{video_name.replace('/', '')}"

    # Download Video from Input bucket
    download_video(s3_client=rgw_s3_client, video_key=video_key, local_path=video_path_on_disk)

    # Extract first frame from video and save on disk
    image_basename = video_name.split(".")[0]
    image_path_on_disk = f"/tmp/{image_basename}.jpeg"
    extract_first_frame_from_video(video_path=video_path_on_disk, image_path=image_path_on_disk)

    # Perform face recognition on image and get student name
    face_rec_result = get_face_rec_result(image_path=image_path_on_disk, encodings_file="/home/app/function/encoding")

    # Fetch student details for the recognized face from DynamoDB
    student_details = get_student_details(dynamo_client=dynamo_client, name=face_rec_result)

    # Save the recognized student record in Output S3 Bucket
    save_results_to_s3(s3_client=rgw_s3_client, filename=image_basename, details=student_details)

    return {
        'statusCode': 200,
        'body': json.dumps({
            'student_details': student_details,
            'video_key': video_key,
            'video_name': video_name
        })
    }
