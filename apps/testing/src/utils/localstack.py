import os
import boto3
import json

# TODO: Move these to a config file
HEADERSECRET=os.environ.get("HEADERSECRET")
os.environ["AWS_ACCESS_KEY_ID"]="123"
os.environ["AWS_SECRET_ACCESS_KEY"]="456"


# https://stackoverflow.com/questions/58828800/adding-custom-headers-to-all-boto3-requests
# Add a custom header to every request (to work with localstack security)

# some_client = boto3.client(service_name=SERVICE_NAME)
# event_system = some_client.meta.events
# event_system.register_first('before-sign.EVENT_NAME.*', _add_header)
# You can try using a wildcard for all requests:
# event_system.register_first('before-sign.*.*', _add_header)

def _add_header(request, **kwargs):
    request.headers.add_header('header-secret', HEADERSECRET)
    print(request.headers)  # for debug


def generate_aws_client(service: str, endpoint_url: str):
    client = boto3.client("s3", endpoint_url=endpoint_url)
    event_system = client.meta.events
    event_system.register_first('before-sign.*.*', _add_header)
    return client


def pp_response(payload: dict) -> None:
    json_formatted_str = json.dumps(payload, indent=2)
    print(json_formatted_str)