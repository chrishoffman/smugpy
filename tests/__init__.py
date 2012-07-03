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
    if sys.version_info < (3,):
        params = req.get_data()
    else:
        params = str( req.get_data(), encoding='utf8' )

    data = makehash()
    data['stat'] = 'ok'
    data['method'] = 'method'

    if 'smugmug.login.' in params:
        data['Login']['Session']['id'] = 123
    elif 'smugmug.auth.get' in params:
        data["Auth"]["Token"]["id"] = 'abc'
        data["Auth"]["Token"]["Secret"] = '123'

    return StringIO(smugpy.json.dumps(data))

smugpy.urlopen = dummy_urlopen