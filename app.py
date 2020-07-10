import json

import boto3
from botocore.exceptions import ClientError

# Load the config file.
with open('conf/config.json', 'r') as f:
    config = json.load(f)

print("Hi,  Welcome to the AWS EC2 security-rules Copier!")

aws_access_key_id = config['ACCESS_KEY']
aws_secret_access_key = config['SECRET_KEY']
region_name = config['REGION_NAME']

# Checking whether the default value is changed.
if aws_access_key_id == 'ACCESS_KEY' or aws_secret_access_key == 'SECRET_KEY' or region_name == 'REGION_NAME' :
    print("Please, Add the config and restart the app.")
    exit()


# getting the ec2 resource.
ec2 = boto3.resource(
    'ec2',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name=region_name
)