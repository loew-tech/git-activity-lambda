import os

import boto3

from activity import sanitize_event
from github import get_recent_events

_SECRET_STRING = "SecretString"
_SECRETS_MANAGER = "secretsmanager"
_GITHUB_TOKEN_SECRET = "GITHUB_TOKEN_SECRET"
_GITHUB_USERNAME = "GITHUB_USERNAME"

secrets_manager = boto3.client(_SECRETS_MANAGER)

def get_github_token() -> str:
    response = secrets_manager.get_secret_value(
        SecretId=os.environ[_GITHUB_TOKEN_SECRET],
    )

    return response[_SECRET_STRING]


def get_github_username() -> str:
    return os.environ[_GITHUB_USERNAME]


def lambda_handler(event, context):
    token, username = get_github_token(), get_github_username()
    events = get_recent_events(token, username)

    return {"events": [sanitize_event(event) for event in events]}