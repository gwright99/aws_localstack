
import sys
sys.dont_write_bytecode = True

# import boto3
from utils.localstack import generate_aws_client, pp_response


endpoint_url = "https://localstack.grahamwrightk8s.net"

# Get buckets
s3 = generate_aws_client("s3", endpoint_url=endpoint_url)
buckets = s3.list_buckets()
pp_response(buckets)

# Create bucket
ec2 = generate_aws_client("ec2", endpoint_url=endpoint_url)


import boto3
from mypy_boto3_s3.client import S3Client
s3: S3Client = boto3.client("s3")
s3.