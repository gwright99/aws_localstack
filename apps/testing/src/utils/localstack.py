import json

from config.logger import logger
from config.getsetvalues import localstack_boto3_header


# REFERNCE
# Add a custom header to every request (to work with localstack security)
# https://stackoverflow.com/questions/58828800/adding-custom-headers-to-all-boto3-requests


def _add_header(request, **kwargs):
    request.headers.add_header('header-secret', localstack_boto3_header) #HEADERSECRET)
    # print(request.headers)  # for debug
    logger.debug(request.headers)


def augment_aws_client_with_http_header(client):
    '''Augment client calls to include the private header value required by the K8s HTTPRoute'''
    event_system = client.meta.events
    event_system.register_first('before-sign.*.*', _add_header)
    return client


# Using decorator for clean emission of payloads
def pp_response(func):
    def wrapper(*args, **kwargs):
        # do something before func
        result = func(*args, **kwargs)
        # do something after func

        # `default=str` added to handle "datetime.datetime not JSON serializable" error
        if result is not None:
            json_formatted_str = print(json.dumps(result, indent=2, default=str))
            return result
    return wrapper