from __future__ import with_statement

from smugpy import SmugMug, SmugMugException
from . import smugpy
import sys
import unittest

API_KEY = "XXXXXXXXXXXXXXXXXXXXXXXXX"
OAUTH_SECRET = "YYYYYYYYYYYYYYYYYYYYYYYY"

class TestSetup(unittest.TestCase):
    def test_no_api_key(self):
        if sys.version_info < (2, 7):
            self.assertRaises(SmugMugException, lambda: SmugMug())
        else:
            with self.assertRaises(SmugMugException):
                SmugMug()

    def test_oauth_not_supported(self):
        if sys.version_info < (2, 7):
            self.assertRaises(SmugMugException, lambda: SmugMug(api_key=API_KEY, oauth_secret=OAUTH_SECRET, api_version="1.2.0"))
        else:
            with self.assertRaises(SmugMugException):
                SmugMug(api_key=API_KEY, oauth_secret=OAUTH_SECRET, api_version="1.2.0")
