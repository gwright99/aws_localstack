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

from config.getsetvalues import endpoint_url


@overload
def get_client(service_name: EC2ServiceName, region_name: str, endpoint_url: Optional[str] = None) -> EC2Client: ...


@overload
def get_client(service_name: S3ServiceName, region_name: str, endpoint_url: Optional[str] = None) -> S3Client: ...


@overload
def get_client(service_name: ServiceName, region_name: str, endpoint_url: Optional[str] = None) -> BaseClient: ...


def get_client(service_name: ServiceName, region_name: str, endpoint_url: Optional[str] = None) -> BaseClient:
    return boto3.client(service_name, region_name=region_name, endpoint_url=endpoint_url)


# type: S3Client, fully type annotated
# All methods and attributes are auto-completed and type checked
# s3_client = get_client("s3", endpoint_url=endpoint_url)

# type: EC2Client, fully type annotated
# All methods and attributes are auto-completed and type checked
# ec2_client = get_client("ec2", endpoint_url=endpoint_url)

# type: BaseClient, only basic type annotations
# Dynamodb-specific methods and attributes are not auto-completed and not type checked
# dynamodb_client = get_client("dynamodb", endpoint_url=endpoint_url)