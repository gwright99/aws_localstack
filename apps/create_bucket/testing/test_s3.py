
import sys
sys.dont_write_bytecode = True
sys.path.insert(0, '../')

import pytest

from time import sleep

from mypy_boto3_ec2.client import EC2Client
from mypy_boto3_s3.client import S3Client
from mypy_boto3_dynamodb.client import DynamoDBClient

from mypy_boto3_s3.literals import BucketLocationConstraintType
from mypy_boto3_s3.type_defs import ListBucketsOutputTypeDef, GetObjectOutputTypeDef

from utils.localstack import pp_response
from config.getsetvalues import endpoint_url, region_name
from utils.aws_client import get_client


# s3_client = get_client("s3", region_name=region_name, endpoint_url=endpoint_url)
# ec2_client = get_client("ec2", region_name=region_name, endpoint_url=endpoint_url)
# dynamodb_client = get_client("dynamodb", region_name=region_name, endpoint_url=endpoint_url)


@pp_response
def helper_get_s3_buckets(s3_client: S3Client) -> ListBucketsOutputTypeDef:
    return s3_client.list_buckets()

bucket_names = ["mybucket1", "mybucket2"]
test_files = (
    ("mybucket1", "files/file1.txt", "ipsem"),
    ("mybucket2", "files/file2.txt", "lorem"),
    ("mybucket1", "logs/log1.log", "abc 123")
)


@pytest.fixture(scope="session")
def s3_client():
    # Setup
    print(f"{__name__} setup")

    yield get_client("s3", region_name=region_name, endpoint_url=endpoint_url)
    
    # Teardown
    print(f"{__name__} teardown")



# @pytest.fixture(scope="module", params=bucket_names)
# def generate_s3_buckets(s3_client, request):
@pytest.fixture(scope="module")
def generate_s3_buckets(s3_client: S3Client):

    # Setup
    print(f"{__name__} setup")
    for bucket_name in bucket_names:
        s3_client.create_bucket(
            Bucket=bucket_name, 
            CreateBucketConfiguration={'LocationConstraint': region_name})
        
    yield

    # # Teardown
    print(f"{__name__} teardown")
    for bucket_name in bucket_names:
        s3_client.delete_bucket(
            Bucket=bucket_name)

    buckets = helper_get_s3_buckets(s3_client)
    assert len(buckets["Buckets"]) == 0


@pytest.fixture(scope="module")
# @pytest.mark.usefixtures('generate_s3_buckets')
def generate_s3_files(s3_client: S3Client, generate_s3_buckets):

    # Setup
    print(f"{__name__} setup")

    for file in test_files:
        bucket, key, content = file
        s3_client.put_object(Bucket=bucket, Key=key, Body=content)

    yield

    # # Teardown
    for file in test_files:
        bucket, key, content = file
        s3_client.delete_object(Bucket=bucket, Key=key)


@pytest.mark.usefixtures('generate_s3_buckets')
def test_all_buckets_created(s3_client):
    buckets = helper_get_s3_buckets(s3_client)
    
    listed_buckets = [bucket["Name"] for bucket in buckets["Buckets"]]
    assert listed_buckets == bucket_names


@pytest.mark.usefixtures('generate_s3_files')
@pytest.mark.parametrize(('bucket', 'key', 'body'), test_files,)
def test_confirm_files_exist(s3_client: S3Client, bucket, key, body):
    myfile: GetObjectOutputTypeDef = s3_client.get_object(Bucket=bucket, Key=key)
    print(myfile)
    assert myfile["Body"].read().decode('utf-8') == body

    sleep(15)


# @pp_response
# def s3_create_bucket(s3_client: S3Client, name: str, region: BucketLocationConstraintType):
#     try:
#         return s3_client.create_bucket(
#             Bucket=name, 
#             CreateBucketConfiguration={'LocationConstraint': region}
#         )
#     except s3_client.exceptions.BucketAlreadyOwnedByYou as e:
#         print(f"Bucket `{name}` already owned by you. Not recreating.")

#     return None 


# def s3_add_file(s3_client: S3Client, filepath: str, bucket: str, key: str):
#     resp = s3_client.put_object(
#         Body=filepath,
#         Bucket=bucket,
#         Key=key
#     )
#     return resp


# @pp_response
# def s3_list_files(s3_client: S3Client, bucket):
#     resp = s3_client.list_objects_v2(
#         Bucket=bucket
#     )
#     return resp


# bucket = 'my-bucket'

# resp = s3_get_buckets(s3_client)
# resp = s3_create_bucket(s3_client, bucket, 'us-west-1')
# resp = s3_add_file(s3_client, "content/somefile.txt", bucket, "somefile.txt")
# resp = s3_list_files(s3_client, bucket)