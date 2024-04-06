# Reference: https://pypi.org/project/mypy-boto3/
from typing import overload
from typing import Optional

import boto3
from botocore.client import BaseClient
from mypy_boto3.literals import ServiceName
from mypy_boto3_ec2.client import EC2Client
from mypy_boto3_ec2.literals import EC2ServiceName
from mypy_boto3_s3.client import S3Client
from mypy_boto3_s3.literals import S3ServiceName
from mypy_boto3_dynamodb.client import DynamoDBClient
from mypy_boto3_dynamodb.literals import DynamoDBServiceName

from utils.localstack import augment_aws_client_with_http_header


@overload
def get_client(service_name: EC2ServiceName, region_name: str, endpoint_url: Optional[str] = None) -> EC2Client: ...

@overload
def get_client(service_name: S3ServiceName, region_name: str, endpoint_url: Optional[str] = None) -> S3Client: ...

@overload
def get_client(service_name: DynamoDBServiceName, region_name: str, endpoint_url: Optional[str] = None) -> DynamoDBClient: ...

@overload
def get_client(service_name: ServiceName, region_name: str, endpoint_url: Optional[str] = None) -> BaseClient: ...

def get_client(service_name: ServiceName, region_name: str, endpoint_url: Optional[str] = None) -> BaseClient:
    client = boto3.client(service_name, region_name=region_name, endpoint_url=endpoint_url)
    augment_aws_client_with_http_header(client)
    return client
