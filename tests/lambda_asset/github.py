import json
import unittest
from unittest.mock import MagicMock, patch

from lambda_asset.github import get_recent_events


class TestGetRecentEvents(unittest.TestCase):

    @patch("lambda_asset.github.urlopen")
    def test_get_recent_events(self, mock_urlopen):
        expected = [
            {
                "type": "PushEvent",
                "repo": {
                    "name": "steve/project",
                },
            }
        ]

        response = MagicMock()
        response.read.return_value = json.dumps(expected).encode()
        mock_urlopen.return_value.__enter__.return_value = response

        actual = get_recent_events("test-token")

        self.assertEqual(expected, actual)

        mock_urlopen.assert_called_once()

    @patch("lambda_asset.github.urlopen")
    def test_get_recent_events_uses_expected_request_headers(self, mock_urlopen):
        response = MagicMock()
        response.read.return_value = b"[]"
        mock_urlopen.return_value.__enter__.return_value = response

        get_recent_events("test-token")

        request = mock_urlopen.call_args.args[0]

        self.assertEqual(
            "application/vnd.github+json",
            request.get_header("Accept"),
        )
        self.assertEqual(
            "Bearer test-token",
            request.get_header("Authorization"),
        )
        self.assertEqual(
            "2022-11-28",
            request.get_header("X-github-api-version"),
        )
        self.assertEqual(
            "github-activity-lambda",
            request.get_header("User-agent"),
        )

    @patch("lambda_asset.github.urlopen")
    def test_get_recent_events_returns_empty_list(self, mock_urlopen):
        response = MagicMock()
        response.read.return_value = b"[]"
        mock_urlopen.return_value.__enter__.return_value = response

        actual = get_recent_events("test-token")

        self.assertEqual([], actual)


if __name__ == "__main__":
    unittest.main()
