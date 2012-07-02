from smugpy import SmugMug, SmugMugException
import smugpy
import unittest
import collections
from StringIO import StringIO

API_KEY = "XXXXXXXXXXXXXXXXXXXXXXXXX"

def makehash():
    return collections.defaultdict(makehash)

def dummy_urlopen(req):
    url = req.get_full_url()
    params = req.get_data()

    data = makehash()
    data['stat'] = 'ok'
    data['method'] = 'method'

    if 'anonymously' in params:
        data['Login']['Session']['id'] = 123

    return StringIO(smugpy.json.dumps(data))

class TestAnonymous(unittest.TestCase):
    def setUp(self):
        self.smugmug = SmugMug(api_key=API_KEY, api_version='1.2.2', app_name='TestApp')

    def test_anonymous_sets_session(self):
        self.smugmug.login_anonymously()
        self.assertEquals(self.smugmug.session_id, 123)

class TestAnonymous130(unittest.TestCase):
    def setUp(self):
        self.smugmug = SmugMug(api_key=API_KEY, api_version='1.3.0', app_name='TestApp')

    def test_anonymous_session(self):
        with self.assertRaises(SmugMugException):
            self.smugmug.login_anonymously()

smugpy.urlopen = dummy_urlopen

if __name__ == '__main__':
    unittest.main()
