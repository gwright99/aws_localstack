
import sys
sys.dont_write_bytecode = True

# import boto3
from utils.localstack import generate_aws_client, pp_response
from config.getsetvalues import endpoint_url, region_name

# type: S3Client, fully type annotated
# All methods and attributes are auto-completed and type checked
s3_client = generate_aws_client("s3", region_name=region_name, endpoint_url=endpoint_url)

# type: EC2Client, fully type annotated
# All methods and attributes are auto-completed and type checked
ec2_client = generate_aws_client("ec2", region_name=region_name, endpoint_url=endpoint_url)

# type: BaseClient, only basic type annotations
# Dynamodb-specific methods and attributes are not auto-completed and not type checked
dynamodb_client = generate_aws_client("dynamodb", region_name=region_name, endpoint_url=endpoint_url)


