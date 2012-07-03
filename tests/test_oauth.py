from __future__ import with_statement

from smugpy import SmugMug, SmugMugException
from . import smugpy
import sys
import unittest

API_KEY = "XXXXXXXXXXXXXXXXXXXXXXXXX"
OAUTH_SECRET = "YYYYYYYYYYYYYYYYYYYYYYYY"

class TestOauth(unittest.TestCase):
    def setUp(self):
        self.smugmug = SmugMug(api_key=API_KEY, api_version='1.2.2', app_name='TestApp', oauth_secret=OAUTH_SECRET)

    def test_get_request_token(self):
        self.smugmug.auth_getRequestToken()
        self.assertNotEqual(self.smugmug.oauth_token, None)
        self.assertNotEqual(self.smugmug.oauth_secret, None)
        self.smugmug.reset_oauth_token()

    def test_get_request_token(self):
        self.smugmug.auth_getAccessToken()
        self.assertNotEqual(self.smugmug.oauth_token, None)
        self.assertNotEqual(self.smugmug.oauth_secret, None)
        self.smugmug.reset_oauth_token()
