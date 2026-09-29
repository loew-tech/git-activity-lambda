import json
import unittest
from unittest.mock import patch, MagicMock

from lambda_asset.github import get_recent_events


class TestGetRecentEvents(unittest.TestCase):

    @patch("lambda_asset.github.urlopen")
    def test_get_recent_events(self, mock_urlopen):
        expected = [
            {
                "type": "PushEvent",
                "repo": {"name": "steve/project"},
            }
        ]

        response = MagicMock()
        response.read.return_value = json.dumps(expected).encode()

        mock_urlopen.return_value.__enter__.return_value = response

        actual = get_recent_events("test-token")

        self.assertEqual(expected, actual)
        mock_urlopen.assert_called_once()


if __name__ == "__main__":
    unittest.main()