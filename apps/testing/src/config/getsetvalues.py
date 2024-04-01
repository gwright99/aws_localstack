import os
import base64
import subprocess


# HEADERSECRET=os.environ.get("HEADERSECRET")
def get_localstack_http_secret(localstack_http_header_secret_name, localstack_http_header_secret_name_ns):
    # Need double {{ to escape the curlies needed by jq }}
    # Need to use `shell=True` since `subprocess.run` won't execute the chained commands
    # Need to convert the secret back to useable string
    
    k8s_secret_command = f"kubectl get secret {localstack_http_header_secret_name} -n {localstack_http_header_secret_ns} -o jsonpath='{{.data}}' | jq '.header' | xargs"
    print(k8s_secret_command)
    http_header_secret_raw = subprocess.run(k8s_secret_command, capture_output=True, shell=True)
    http_header_secret_decoded = base64.b64decode(http_header_secret_raw.stdout.decode("UTF8").strip()).decode("UTF8")
    return http_header_secret_decoded


os.environ["AWS_ACCESS_KEY_ID"]="123"
os.environ["AWS_SECRET_ACCESS_KEY"]="456"

# Point to localstack instead of regular AWS
endpoint_url = "https://localstack.grahamwrightk8s.net"
region_name = "us-east-1"

# K8s secrets
localstack_http_header_secret_name = "header-secret"
localstack_http_header_secret_ns = "localstack"

localstack_boto3_header = get_localstack_http_secret(localstack_http_header_secret_name, localstack_http_header_secret_ns)



