
import sys
sys.dont_write_bytecode = True

from mypy_boto3_ec2.client import EC2Client
from mypy_boto3_s3.client import S3Client
from mypy_boto3_dynamodb.client import DynamoDBClient

from mypy_boto3_s3.literals import BucketLocationConstraintType

from utils.localstack import pp_response
from config.getsetvalues import endpoint_url, region_name
from utils.aws_client import get_ec2_client, get_s3_client, get_dynamodb_client

s3_client = get_s3_client("s3", region_name=region_name, endpoint_url=endpoint_url)
ec2_client = get_ec2_client("ec2", region_name=region_name, endpoint_url=endpoint_url)
dynamodb_client = get_dynamodb_client("dynamodb", region_name=region_name, endpoint_url=endpoint_url)


@pp_response
def s3_get_buckets(s3_client: S3Client):
    return s3_client.list_buckets()

@pp_response
def s3_create_bucket(s3_client: S3Client, name: str, region: BucketLocationConstraintType):
    try:
        return s3_client.create_bucket(
            Bucket=name, 
            CreateBucketConfiguration={'LocationConstraint': region}
        )
    except s3_client.exceptions.BucketAlreadyOwnedByYou as e:
        print(f"Bucket `{name}` already owned by you. Not recreating.")

    return None 


resp = s3_get_buckets(s3_client)
resp = s3_create_bucket(s3_client, 'my-bucket', 'us-west-1')