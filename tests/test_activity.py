import unittest

from lambda_asset.activity import sanitize_event


class TestSanitizeEvent(unittest.TestCase):

    def test_sanitizes_public_event(self):
        event = {
            "type": "PushEvent",
            "public": True,
            "created_at": "2026-10-01T15:20:00Z",
            "repo": {
                "name": "steve/public-project",
            },
        }

        expected = {
            "type": "PushEvent",
            "repository": "steve/public-project",
            "public": True,
            "timestamp": "2026-10-01T15:20:00Z",
        }

        actual = sanitize_event(event)

        self.assertEqual(expected, actual)

    def test_sanitizes_private_event(self):
        event = {
            "type": "PushEvent",
            "public": False,
            "created_at": "2026-10-01T15:20:00Z",
            "repo": {
                "name": "steve/private-project",
            },
        }

        expected = {
            "type": "PushEvent",
            "public": False,
            "timestamp": "2026-10-01T15:20:00Z",
        }

        actual = sanitize_event(event)

        self.assertEqual(expected, actual)

    def test_private_event_does_not_expose_repository(self):
        event = {
            "type": "PushEvent",
            "public": False,
            "created_at": "2026-10-01T15:20:00Z",
            "repo": {
                "name": "steve/private-project",
            },
        }

        actual = sanitize_event(event)

        self.assertNotIn("repository", actual)
        self.assertNotIn("private-project", str(actual))


if __name__ == "__main__":
    unittest.main()
