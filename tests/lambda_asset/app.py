import unittest
from unittest.mock import patch

from lambda_asset.app import lambda_handler


class TestLambdaHandler(unittest.TestCase):

    @patch("lambda_asset.app.get_recent_events")
    def test_lambda_handler_returns_github_events(self, mock_get_recent_events):
        expected = [
            {
                "type": "PushEvent",
                "repo": {
                    "name": "steve/project",
                },
            }
        ]
        mock_get_recent_events.return_value = expected

        with patch.dict("os.environ", {"GITHUB_TOKEN": "test-token"}):
            actual = lambda_handler({}, None)

        self.assertEqual({"events": expected}, actual)
        mock_get_recent_events.assert_called_once_with("test-token")

    @patch("lambda_asset.app.get_recent_events")
    def test_lambda_handler_returns_empty_events(self, mock_get_recent_events):
        expected = []
        mock_get_recent_events.return_value = expected

        with patch.dict("os.environ", {"GITHUB_TOKEN": "test-token"}):
            actual = lambda_handler({}, None)

        self.assertEqual({"events": expected}, actual)
        mock_get_recent_events.assert_called_once_with("test-token")


if __name__ == "__main__":
    unittest.main()
