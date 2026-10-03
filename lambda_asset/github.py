import json
from urllib.request import Request, urlopen

GITHUB_API_URL = "https://api.github.com"
GITHUB_API_VERSION = "2022-11-28"


def get_recent_events(token: str) -> list[dict]:
    request = Request(
        f"{GITHUB_API_URL}/user/events",
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "X-Github-Api-Version": GITHUB_API_VERSION,
            "User-Agent": "github-activity-lambda",
        },
    )

    with urlopen(request) as response:
        return json.loads(response.read().decode())