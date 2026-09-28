import unittest

from daily_arxiv import settings


class SettingsTests(unittest.TestCase):
    def test_retry_http_codes_include_429_and_406(self):
        self.assertIn(429, settings.RETRY_HTTP_CODES)
        self.assertIn(406, settings.RETRY_HTTP_CODES)
        self.assertGreater(settings.RETRY_TIMES, 0)

    def test_user_agent_is_configured(self):
        self.assertTrue(settings.USER_AGENT)
