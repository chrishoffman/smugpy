import smugpy
import sys
import collections

try: 
    from StringIO import StringIO
except:
    from io import StringIO

def makehash():
    return collections.defaultdict(makehash)

def dummy_urlopen(req):
    url = req.get_full_url()
    params = req.get_data()
    method = req.get_method()

    data = makehash()
    data['stat'] = 'ok'
    data['method'] = 'method'

    if 'upload.smugmug.com' in url:
        data['Image']['id'] = 321
        del data['method']
    else:
        if sys.version_info >= (3,):
            params = params.decode('utf-8')

        if 'smugmug.login.' in params:
            data['Login']['Session']['id'] = 123
        elif 'smugmug.auth.get' in params:
            data["Auth"]["Token"]["id"] = 'abc'
            data["Auth"]["Token"]["Secret"] = '123'
        elif 'smugmug.albums.get' in params:
            data['method'] = 'smugmug.albums.get'
        elif 'smugmug.bad.apimethod' in params:
            data['stat'] = 'fail'
            data['code'] = 999
            data['message'] = 'Method does not exist'

    return StringIO(smugpy.json.dumps(data))

smugpy.urlopen = dummy_urlopen