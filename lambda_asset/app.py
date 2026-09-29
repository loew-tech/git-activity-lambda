import os

from lambda_asset.github import get_recent_events


def lambda_handler(event, context):
    events = get_recent_events(os.environ["GITHUB_TOKEN"])

    return {"events": events}