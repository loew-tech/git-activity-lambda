import unittest
from unittest.mock import patch

from lambda_asset.app import lambda_handler


class TestLambdaHandler(unittest.TestCase):

    @patch("lambda_asset.app.sanitize_event")
    @patch("lambda_asset.app.get_recent_events")
    @patch("lambda_asset.app.get_github_token")
    def test_lambda_handler_returns_github_events(
        self,
        mock_get_github_token,
        mock_get_recent_events,
        mock_sanitize_event,
    ):
        github_token = "test-token"

        events = [
            {
                "type": "PushEvent",
                "public": True,
            },
            {
                "type": "PushEvent",
                "public": False,
            },
        ]

        expected_events = [
            {
                "type": "PushEvent",
                "repository": "steve/public-project",
                "public": True,
            },
            {
                "type": "PushEvent",
                "public": False,
            },
        ]

        mock_get_github_token.return_value = github_token
        mock_get_recent_events.return_value = events
        mock_sanitize_event.side_effect = expected_events

        actual = lambda_handler({}, None)

        self.assertEqual(
            {"events": expected_events},
            actual,
        )

        mock_get_github_token.assert_called_once_with()
        mock_get_recent_events.assert_called_once_with(github_token)

        self.assertEqual(
            2,
            mock_sanitize_event.call_count,
        )

        mock_sanitize_event.assert_any_call(events[0])
        mock_sanitize_event.assert_any_call(events[1])

    @patch("lambda_asset.app.sanitize_event")
    @patch("lambda_asset.app.get_recent_events")
    @patch("lambda_asset.app.get_github_token")
    def test_lambda_handler_returns_empty_events(
        self,
        mock_get_github_token,
        mock_get_recent_events,
        mock_sanitize_event,
    ):
        mock_get_github_token.return_value = "test-token"
        mock_get_recent_events.return_value = []

        actual = lambda_handler({}, None)

        self.assertEqual(
            {"events": []},
            actual,
        )

        mock_get_github_token.assert_called_once_with()
        mock_get_recent_events.assert_called_once_with("test-token")
        mock_sanitize_event.assert_not_called()


if __name__ == "__main__":
    unittest.main()
