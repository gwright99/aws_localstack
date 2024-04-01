import json
from typing import Optional

from utils.aws_client import get_client
from config.getsetvalues import localstack_boto3_header #HEADERSECRET
from mypy_boto3.literals import ServiceName


# REFERNCE
# Add a custom header to every request (to work with localstack security)
# https://stackoverflow.com/questions/58828800/adding-custom-headers-to-all-boto3-requests


def _add_header(request, **kwargs):
    request.headers.add_header('header-secret', localstack_boto3_header) #HEADERSECRET)
    print(request.headers)  # for debug


def generate_aws_client(service_name: ServiceName, region_name: str, endpoint_url: Optional[str] = None):
    '''Augment client calls to include the private header value required by the K8s HTTPRoute'''
    client = get_client(service_name, region_name=region_name, endpoint_url=endpoint_url)
    event_system = client.meta.events
    event_system.register_first('before-sign.*.*', _add_header)
    return client


def pp_response(payload: dict) -> None:
    '''Pretty print the verbose json output'''
    # `default=str` added to handle "datetime.datetime not JSON serializable" error
    json_formatted_str = json.dumps(payload, indent=2, default=str)
    print(json_formatted_str)