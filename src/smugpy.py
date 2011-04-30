import binascii
import hashlib
import hmac
import time
import urllib
import urlparse
import uuid
import functools

try:
    import simplejson
except ImportError:
    from django.utils import simplejson

def _authenticated(method):
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        if self.oauth_token is None and self.session_id is None:
            raise SmugMugException, "Authentication required for this method"
            
        return method(self, *args, **kwargs)
    return wrapper


class SmugMug(object):
    def __init__(self, api_key=None, oauth_secret=None, api_version="1.3.0", secure=False,
                 session_id=None, oauth_token=None, oauth_token_secret=None):
        """Initializes a session."""
        self.api_key = api_key
        self.oauth_secret = oauth_secret
        self.api_version = api_version
        self.secure = secure
        self.session_id = session_id
        self.oauth_token = oauth_token
        self.oauth_token_secret = oauth_token_secret
        
        if api_key is None: 
            raise SmugMugException, "API Key is Required"
        
        if oauth_secret is not None and api_version != "1.2.2":
            raise SmugMugException, "Oauth only supported in version 1.2.2"

    @_authenticated
    def __getattr__(self, method, **args):
        """Construct a dynamic handler for the SmugMug API.

        This function handles all SmugMug method call not explicitly
        implemented.  Authentication is required before making any
        calls here.
        """
        return self._make_handler(method)

    def set_oauth_token(self, token, secret):
        """Sets the OAuth access token for this session."""
        self.oauth_token = token
        self.oauth_token_secret = secret

    def reset_oauth_token(self):
        """Resets the OAuth access token"""
        self.oauth_token = None
        self.oauth_token_secret = None

    def set_session(self, session_id):
        """Sets the id for this session."""
        self.session_id = session_id

    def service_ping(self):
        kwargs = dict(APIKey=self.api_key)
        ping = self._make_handler("service_ping")
        return ping(**kwargs)

    #Login methods
    def _login(self, handler, **kwargs):
        """General login method that stores returned session id"""
        kwargs.update(dict(APIKey=self.api_key))
        login = self._make_handler(handler)
        rsp = login(**kwargs)
        self.set_session(rsp["Login"]["Session"]["id"])
        return rsp

    def login_anonymously(self, **kwargs):
        return self._login("login_anonymously", **kwargs)

    def login_withHash(self, **kwargs):
        return self._login("login_withHash", **kwargs)

    def login_withPassword(self, **kwargs):
        return self._login("login_withPassword", **kwargs)

    def auth_getRequestToken(self, **kwargs):
        auth = self._make_handler("auth_getRequestToken")
        rsp = auth(**kwargs)
        self.set_oauth_token(rsp["Auth"]["Token"]["id"],
            rsp["Auth"]["Token"]["Secret"])
        return rsp

    @_authenticated
    def auth_getAccessToken(self, **kwargs):
        auth = self._make_handler("auth_getAccessToken")
        rsp = auth(**kwargs)
        self.set_oauth_token(rsp["Auth"]["Token"]["id"],
            rsp["Auth"]["Token"]["Secret"])
        return rsp

    def _make_handler(self, method):
        if method.startswith("login_with") or self.secure:
            proto = "https"
        else:
            proto = "http"
        method = "smugmug." + method.replace("_", ".")
        
        def api_request(**kwargs):
            """Fetches the given API call"""
            url = proto + "://api.smugmug.com/services/api/json/" + self.api_version + "/"
            kwargs.update(dict(method=method))
            
            # Add the OAuth resource request signature if we have credentials
            if self.oauth_secret:
                all_args={}
                all_args.update(kwargs)
                oauth = self._get_oauth_resource_request_parameters(url, all_args, method="GET")
                kwargs.update(oauth)
            elif self.session_id:
                kwargs.update(dict(SessionID=self.session_id))
            
            if kwargs: url += "?" + urllib.urlencode(kwargs)
            rsp = self._fetch_url(url)
            
            return self._handle_response(rsp)
        
        return api_request

    def _handle_response(self, response):
        parsed = simplejson.loads(response.decode("UTF-8"))
        #TODO: Add better error handling
        if parsed["stat"] == "fail":
            raise SmugMugException, "SmugMug API Error for method " + parsed["method"] + \
                ": (" + str(parsed["code"]) + ") " + parsed["message"]

        return parsed
    
    #Oauth methods
    def authorize(self, access="Public", perm="Read"):
        """Returns the SmugMug authorization URL for the given request token."""
        return "http://api.smugmug.com/services/oauth/authorize.mg?" + \
            urllib.urlencode(dict(oauth_token=self.oauth_token)) + \
            "&Access=" + access + "&Permissions=" + perm

    def _get_oauth_resource_request_parameters(self, url, parameters={}, method="GET"):
        """Returns the OAuth parameters as a dict for the given resource request."""
        base_args = dict(
            oauth_consumer_key=self.api_key,
            oauth_signature_method="HMAC-SHA1",
            oauth_timestamp=str(int(time.time())),
            oauth_nonce=binascii.b2a_hex(uuid.uuid4().bytes),
            oauth_version="1.0",
        )
        if self.oauth_token: base_args["oauth_token"]=self.oauth_token
        args = {}
        args.update(base_args)
        args.update(parameters)
        signature = self._oauth_signature(method, url, args)
        base_args["oauth_signature"] = signature
        return base_args

    def _oauth_signature(self, method, url, parameters={}):
        """Calculates the HMAC-SHA1 OAuth signature for the given request."""
        parts = urlparse.urlparse(url)
        proto, netloc, path = parts[:3]
        normalized_url = proto.lower() + "://" + netloc.lower() + path
        
        base_elems = []
        base_elems.append(method.upper())
        base_elems.append(normalized_url)
        base_elems.append("&".join("%s=%s" % (k, urlencodeRFC3986(str(v)))
                                   for k, v in sorted(parameters.items())))
        base_string =  "&".join(urlencodeRFC3986(e) for e in base_elems)
        
        key_elems = [self.oauth_secret]
        key_elems.append(self.oauth_token_secret if self.oauth_token_secret else "")
        key = "&".join(key_elems)
        
        hash = hmac.new(key, base_string, hashlib.sha1)
        return binascii.b2a_base64(hash.digest())[:-1]
    
    def _fetch_url(self, url):
        import urllib2
        #TODO: Add useragent header
        return urllib2.urlopen(url).read()

def urlencodeRFC3986(val):
    if isinstance(val, unicode):
        val = val.encode("utf-8")
    return urllib.quote(val, safe="~")
    
    
class SmugMugException(Exception):
    """SmugMug specific exception"""
    pass

if __name__ == '__main__':
    pass
