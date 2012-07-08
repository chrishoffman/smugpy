import sys

try:
    import urllib.request as urlrequest
    from urllib.request import urlopen
    from urllib.parse import urlparse, quote, urlencode
except ImportError:
    import urllib2 as urlrequest
    from urllib2 import urlopen
    from urlparse import urlparse
    from urllib import quote, urlencode

try:
    import simplejson as json
except ImportError:
    import json
except ImportError:
    from django.utils import simplejson as json

def compat_decode(val):
    if sys.version_info < (3,) and isinstance(val, unicode):
        return val.decode('utf-8')
    elif sys.version_info >= (3,) and isinstance(val, bytes):
        return val.decode('utf-8')
    else:
        return val

def compat_encode(val):
    if sys.version_info < (3,) and isinstance(val, unicode):
        return val.encode('utf-8')
    elif sys.version_info >= (3,) and isinstance(val, str):
        return val.encode('utf-8')
    else:
        return val
