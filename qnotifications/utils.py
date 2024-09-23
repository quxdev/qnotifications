import os
from functools import wraps
import boto3
from botocore.exceptions import ClientError
from botocore.config import Config


def configure_aws_credentials(aws_access_key_id, aws_secret_access_key, region_name):
    boto3.setup_default_session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=region_name
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
