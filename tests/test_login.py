from __future__ import with_statement

from smugpy import SmugMug, SmugMugException
from . import smugpy
import sys
import unittest

API_KEY = "XXXXXXXXXXXXXXXXXXXXXXXXX"

class TestLogin(unittest.TestCase):
    def setUp(self):
        self.smugmug = SmugMug(api_key=API_KEY, api_version='1.2.2', app_name='TestApp')

    def test_login_anonymously(self):
        self.smugmug.login_anonymously()
        self.assertNotEqual(self.smugmug.session_id, None)
        self.smugmug.reset_auth()

    def test_login_withHash(self):
        self.smugmug.login_withHash(UserID='test', PasswordHash='ABCDE')
        self.assertNotEqual(self.smugmug.session_id, None)
        self.smugmug.reset_auth()

    def test_login_withPassword(self):
        self.smugmug.login_withPassword(EmailAddress='test@example.com', Password='ABC123')
        self.assertNotEqual(self.smugmug.session_id, None)
        self.smugmug.reset_auth()

class TestLogin130(unittest.TestCase):
    def setUp(self):
        self.smugmug = SmugMug(api_key=API_KEY, api_version='1.3.0', app_name='TestApp')

    def test_login_anonymously(self):
        if sys.version_info < (2, 7):
            self.assertRaises(SmugMugException, lambda: self.smugmug.login_anonymously())
        else:
            with self.assertRaises(SmugMugException):
                self.smugmug.login_anonymously()

    def test_login_withHash(self):
        if sys.version_info < (2, 7):
            self.assertRaises(SmugMugException, lambda: self.smugmug.login_withHash(UserID='test', PasswordHash='ABCDE'))
        else:
            with self.assertRaises(SmugMugException):
                self.smugmug.login_withHash(UserID='test', PasswordHash='ABCDE')

    def test_login_withPassword(self):
        if sys.version_info < (2, 7):
            self.assertRaises(SmugMugException, lambda: self.smugmug.login_withPassword(EmailAddress='test@example.com', Password='ABC123'))
        else:
            with self.assertRaises(SmugMugException):
                self.smugmug.login_withPassword(EmailAddress='test@example.com', Password='ABC123')
