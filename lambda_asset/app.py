import os

import boto3

from lambda_asset.activity import sanitize_event
from lambda_asset.github import get_recent_events

_SECRET_STRING = "SecretString"
_SECRETS_MANAGER = "secretsmanager"
_GITHUB_TOKEN_SECRET = "GITHUB_TOKEN_SECRET"

secrets_manager = boto3.client(_SECRETS_MANAGER)

def get_github_token() -> str:
    response = secrets_manager.get_secret_value(
        SecretId=os.environ[_GITHUB_TOKEN_SECRET],
    )

    return response[_SECRET_STRING]


def lambda_handler(event, context):
    token = get_github_token()
    events = get_recent_events(token)

    return {"events": [sanitize_event(event) for event in events]}