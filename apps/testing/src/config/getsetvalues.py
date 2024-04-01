import os

HEADERSECRET=os.environ.get("HEADERSECRET")

os.environ["AWS_ACCESS_KEY_ID"]="123"
os.environ["AWS_SECRET_ACCESS_KEY"]="456"

# Point to localstack instead of regular AWS
endpoint_url = "https://localstack.grahamwrightk8s.net"
region_name = "us-east-1"