import os
import base64
import logging
import subprocess


# https://www.loggly.com/ultimate-guide/python-logging-basics/
logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler()) # Writes to console
logger.setLevel(os.environ.get("APP_LOGLEVEL", "INFO"))
# https://stackoverflow.com/questions/1661275/disable-boto-logging-without-modifying-the-boto-files
logging.getLogger('boto3').setLevel(logging.CRITICAL)
logging.getLogger('botocore').setLevel(logging.CRITICAL)
logging.getLogger('s3transfer').setLevel(logging.CRITICAL)
logging.getLogger('urllib3').setLevel(logging.CRITICAL)


# HEADERSECRET=os.environ.get("HEADERSECRET")
def get_localstack_http_secret(localstack_http_header_secret_name, localstack_http_header_secret_name_ns):
    # Need double {{ to escape the curlies needed by jq }}
    # Need to use `shell=True` since `subprocess.run` won't execute the chained commands
    # Need to convert the secret back to useable string
    
    k8s_secret_command = f"kubectl get secret {localstack_http_header_secret_name} -n {localstack_http_header_secret_ns} -o jsonpath='{{.data}}' | jq '.header' | xargs"
    print(k8s_secret_command)
    http_header_secret_raw = subprocess.run(k8s_secret_command, capture_output=True, shell=True)
    http_header_secret_decoded = base64.b64decode(http_header_secret_raw.stdout.decode("UTF8").strip())
    http_header_secret_decoded_raw = http_header_secret_decoded.decode("UTF8").strip()
    return http_header_secret_decoded_raw


os.environ["AWS_ACCESS_KEY_ID"]="123"
os.environ["AWS_SECRET_ACCESS_KEY"]="456"

# Point to localstack instead of regular AWS
endpoint_url = "https://localstack.grahamwrightk8s.net"
region_name = "us-east-2"

# K8s secrets
localstack_http_header_secret_name = "header-secret"
localstack_http_header_secret_ns = "localstack"

localstack_boto3_header = get_localstack_http_secret(localstack_http_header_secret_name, localstack_http_header_secret_ns)



