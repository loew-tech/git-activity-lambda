import json
from urllib.request import Request, urlopen

from urllib3.exceptions import HTTPError

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

    try:
        with urlopen(request) as response:
            data = json.loads(response.read().decode())
            print(f'{data=}')
            return data
            # return json.loads(response.read().decode())
    except Exception as err:
        print(f'{err=}')
        return []