from __future__ import with_statement

from smugpy import SmugMug, SmugMugException
from . import smugpy
import sys
import unittest

API_KEY = "XXXXXXXXXXXXXXXXXXXXXXXXX"
OAUTH_SECRET = "YYYYYYYYYYYYYYYYYYYYYYYY"

class TestApi(unittest.TestCase):
    def setUp(self):
        self.smugmug = SmugMug(api_key=API_KEY, api_version='1.2.2', app_name='TestApp')

    def test_ping(self):
        rsp = self.smugmug.service_ping()
        self.assertEqual(rsp['stat'], 'ok')

    def test_dynamic_method(self):
        self.smugmug.login_anonymously()
        rsp = self.smugmug.albums_get(NickName='test')
        self.assertEqual(rsp['method'], 'smugmug.albums.get')
        self.smugmug.reset_auth()

    def test_authorize(self):
        expected = 'http://api.smugmug.com/services/oauth/authorize.mg?oauth_token=ABC&Access=Public&Permissions=Read'
        self.smugmug.set_oauth_token('ABC','123')
        url = self.smugmug.authorize(access='Public', perm='Read')
        self.assertEqual(url, expected)
        self.smugmug.reset_auth()

    def test_failed_api(self):
        if sys.version_info < (2, 7):
            self.assertRaises(SmugMugException, lambda: self.smugmug.bad_apimethod())
        else:
            with self.assertRaises(SmugMugException):
                self.smugmug.bad_apimethod()

class TestApi130(unittest.TestCase):
    def setUp(self):
        self.smugmug = SmugMug(api_key=API_KEY, api_version='1.3.0', app_name='TestApp')

    def test_anonymous_dynamic_method(self):
        rsp = self.smugmug.albums_get(NickName='test')
        self.assertEqual(rsp['method'], 'smugmug.albums.get')

class TestApiImageUpload(unittest.TestCase):
    def setUp(self):
        self.smugmug = SmugMug(api_key=API_KEY, api_version='1.2.2', app_name='TestApp')

    def test_image_upload_missing_param(self):
        self.smugmug.login_withHash(UserID='test', PasswordHash='ABCDE')
        if sys.version_info < (2, 7):
            self.assertRaises(SmugMugException, lambda: self.smugmug.images_upload())
        else:
            with self.assertRaises(SmugMugException):
                self.smugmug.images_upload()
        self.smugmug.reset_auth()

    def test_image_upload_without_auth(self):
        if sys.version_info < (2, 7):
            self.assertRaises(SmugMugException, lambda: self.smugmug.images_upload(File='tests/smuggy.jpg', AlbumID=1234))
        else:
            with self.assertRaises(SmugMugException):
                self.smugmug.images_upload(File='tests/smuggy.jpg', AlbumID=1234)
        self.smugmug.reset_auth()

    def test_image_upload(self):
        self.smugmug.login_withHash(UserID='test', PasswordHash='ABCDE')
        rsp = self.smugmug.images_upload(File='tests/smuggy.jpg', AlbumID=1234)
        self.assertEqual(rsp['method'], 'smugmug.images.upload')
        self.smugmug.reset_auth()

    def test_image_upload_with_filename(self):
        self.smugmug.login_withHash(UserID='test', PasswordHash='ABCDE')
        rsp = self.smugmug.images_upload(File='tests/smuggy.jpg', AlbumID=1234, FileName='rename.jpg')
        self.assertEqual(rsp['method'], 'smugmug.images.upload')
        self.smugmug.reset_auth()

class TestApiImageUploadOauth(unittest.TestCase):
    def setUp(self):
        self.smugmug = SmugMug(api_key=API_KEY, api_version='1.3.0', app_name='TestApp', oauth_secret=OAUTH_SECRET)

    def test_image_upload_oauth(self):
        self.smugmug.set_oauth_token('ABC','123')
        rsp = self.smugmug.images_upload(File='tests/smuggy.jpg', AlbumID=1234)
        self.assertEqual(rsp['method'], 'smugmug.images.upload')
        self.smugmug.reset_auth()
