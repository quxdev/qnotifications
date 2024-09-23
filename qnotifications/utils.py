import os
from functools import wraps
import boto3
from botocore.exceptions import ClientError


def configure_aws_credentials(
    aws_access_key_id=None, aws_secret_access_key=None, region_name=None
):
    if aws_access_key_id and aws_secret_access_key:
        boto3.setup_default_session(
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region_name
            or os.environ.get("AWS_DEFAULT_REGION", "us-east-1"),
        )
    elif "AWS_ACCESS_KEY_ID" in os.environ and "AWS_SECRET_ACCESS_KEY" in os.environ:
        # Credentials are already set in environment variables
        pass
    else:
        # Use the default credential provider chain
        boto3.setup_default_session(
            region_name=region_name or os.environ.get("AWS_DEFAULT_REGION", "us-east-1")
        )


def handle_aws_error(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ClientError as e:
            error_code = e.response["Error"]["Code"]
            error_message = e.response["Error"]["Message"]
            raise Exception(f"AWS Error ({error_code}): {error_message}") from e

    return wrapper
