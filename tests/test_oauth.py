from __future__ import with_statement

from smugpy import SmugMug, SmugMugException
from . import smugpy
import sys
import unittest

API_KEY = 'XXXXXXXXXXXXXXXXXXXXXXXXX'
OAUTH_SECRET = 'YYYYYYYYYYYYYYYYYYYYYYYY'

class TestOauth(unittest.TestCase):
    def setUp(self):
        self.smugmug = SmugMug(api_key=API_KEY, api_version='1.3.0', app_name='TestApp', oauth_secret=OAUTH_SECRET)

    def test_get_request_token(self):
        self.smugmug.auth_getRequestToken()
        self.assertNotEqual(self.smugmug.oauth_token, None)
        self.assertNotEqual(self.smugmug.oauth_token_secret, None)
        self.smugmug.reset_auth()

    def test_get_access_token(self):
        self.smugmug.auth_getAccessToken()
        self.assertNotEqual(self.smugmug.oauth_token, None)
        self.assertNotEqual(self.smugmug.oauth_token_secret, None)
        self.smugmug.reset_auth()

    def test_request_signature(self):
        url = 'http://api.smugmug.com/services/api/json/'
        parameters = dict(
            method = 'smugmug.albums.get',
            NickName = 'williams'
        )
        timestamp = 1341423551
        nonce = 'b7cdabcabc3c4f7f91508da3bca9798f'
        signed_args = self.smugmug._get_oauth_request_params(url=url, parameters=parameters, method='POST', timestamp=timestamp, nonce=nonce)
        self.assertEqual(signed_args['oauth_signature'], 'f++GOXf9BhSVhGy1dxGSbmaA0ng=')
