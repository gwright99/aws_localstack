import sys
sys.dont_write_bytecode = True

from mypy_boto3_ec2.client import EC2Client
from mypy_boto3_s3.client import S3Client
from mypy_boto3_dynamodb.client import DynamoDBClient

from mypy_boto3_s3.literals import BucketLocationConstraintType

from utils.localstack import pp_response
from config.getsetvalues import endpoint_url, region_name
# from utils.aws_client import get_ec2_client, get_s3_client, get_dynamodb_client
from utils.aws_client import get_client