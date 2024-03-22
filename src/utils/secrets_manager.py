import json
import boto3
from botocore.exceptions import ClientError

from src.utils.secrets import secrets


def get_secret(secret_name: str) -> dict:
    session = boto3.session.Session()
    client = session.client(service_name='secretsmanager', region_name=secrets['AWS']['region'])

    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    except ClientError as e:
        raise e

    secret = get_secret_value_response['SecretString']

    return json.loads(secret)
