import boto3
from botocore.config import Config
import os

access_key = 'AU18J6SD0PU9YDWK0IHM'
secret_key = '5jbeV6owq1g5ByCRDHH4PfN6IvhRhAMFjYwGgWEU'
endpoint_url = 'http://192.168.49.2:31995'
input_bucket = 'ceph-bkt-input-blankspace'
output_bucket = 'ceph-bkt-output-blankspace'
local_file_path = 'file.txt'  # Replace with the path to your file
object_key = 'example_object.txt'  # Replace with the object key/name

config = Config(signature_version='s3v4', s3={'addressing_style': 'path'})

rgw_s3_client = boto3.client('s3',
                             endpoint_url=endpoint_url, 
                             aws_access_key_id=access_key, 
                             aws_secret_access_key=secret_key,
                             config=config)

#rgw_s3_client.create_bucket(Bucket=bucket_name2)

#print(rgw_s3_client.list_buckets())

def clear_output_bucket():
	global output_bucket
	s3 = rgw_s3_client
	list_obj = s3.list_objects_v2(Bucket=output_bucket)
	try:
		for item in list_obj["Contents"]:
			key = item["Key"]
			print(f"Deleting: {key} from {output_bucket}")
			s3.delete_object(Bucket=output_bucket, Key=key)
	except:
		print("Nothing to clear in output bucket")
		
def clear_input_bucket():
	global output_bucket
	s3 = rgw_s3_client
	list_obj = s3.list_objects_v2(Bucket=input_bucket)
	try:
		for item in list_obj["Contents"]:
			key = item["Key"]
			print(f"Deleting: {key} from {input_bucket}")
			s3.delete_object(Bucket=input_bucket, Key=key)
	except:
		print("Nothing to clear in output bucket")

def upload_to_input_bucket_s3(path, name):
	global input_bucket
	s3 = rgw_s3_client
	s3.upload_file(path + name, input_bucket, name)

def upload_files(test_case):	
	global input_bucket
	global output_bucket
	test_cases = "test_cases/"
	
	
	# Directory of test case
	test_dir = test_cases + test_case + "/"
	
	# Iterate over each video
	# Upload to S3 input bucket
	for filename in os.listdir(test_dir):
		if filename.endswith(".mp4") or filename.endswith(".MP4"):
			print("Uploading to input bucket..  name: " + str(filename)) 
			upload_to_input_bucket_s3(test_dir, filename)
			

clear_output_bucket()
clear_input_bucket()
print("Running Test Case 2")
upload_files("test_case_2")
