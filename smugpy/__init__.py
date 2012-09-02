#!/usr/bin/env python
# -*- coding: utf-8 -*-

import binascii
import hashlib
import hmac
import time
import uuid
import os

from .portability import urlencode, urlparse, urlrequest, urlopen, quote, \
    json, compat_decode, compat_encode

__version__ = "0.3.1"


class SmugMug(object):
    def __init__(self, api_key=None, oauth_secret=None, api_version="1.3.0",
                 secure=False, session_id=None, oauth_token=None,
                 oauth_token_secret=None, app_name="Unknown App"):
        """Initializes a session."""
        self.api_key = api_key
        self.oauth_secret = oauth_secret
        self.secure = secure
        self.session_id = session_id
        self.oauth_token = oauth_token
        self.oauth_token_secret = oauth_token_secret
        self.application = "%s (smugpy/%s)" % (app_name, __version__)
        self.api_version = api_version

        if api_key is None:
            raise SmugMugException("API Key is Required")

        if oauth_secret is not None and not self.check_version(min="1.2.2"):
            raise SmugMugException("Oauth only supported in \
                                   API versions 1.2.2+")

    def __getstate__(self):  # pragma: no cover
        """Provide getstate for pickling the object.

        Without __getstate__ pickle will try to use __getattr__ which has
        side-effects unexpected by pickle
        """
        return self.__dict__

    def __setstate__(self, state):  # pragma: no cover
        """Provide setstate for unpickling"""
        self.__dict__.update(state)

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

    def reset_auth(self):
        """Resets the authorization"""
        self.oauth_token = None
        self.oauth_token_secret = None
        self.session_id = None

    def set_session(self, session_id):
        """Sets the id for this session."""
        self.session_id = session_id

    def service_ping(self):
        """Ping service to check the current API status"""
        kwargs = dict(APIKey=self.api_key)
        ping = self._make_handler("service_ping")
        return ping(**kwargs)

    # Login methods (1.2.2 and lower)
    def _login(self, handler, **kwargs):
        """General login method that stores returned session id"""
        # Beginning in 1.3.0, Oauth and anonymous are the only supported
        # authentication methods and no session is required for anonymous
        # access
        if not self.check_version(max="1.2.2"):
            raise SmugMugException("Not a supported method")

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
        """Obtain an Oauth request token"""
        auth = self._make_handler("auth_getRequestToken")
        rsp = auth(**kwargs)
        self.set_oauth_token(rsp["Auth"]["Token"]["id"],
                             rsp["Auth"]["Token"]["Secret"])
        return rsp

    def auth_getAccessToken(self, **kwargs):
        """Obtain an Oauth access token"""
        auth = self._make_handler("auth_getAccessToken")
        rsp = auth(**kwargs)
        self.set_oauth_token(rsp["Auth"]["Token"]["id"],
                             rsp["Auth"]["Token"]["Secret"])
        return rsp

    def images_upload(self, **kwargs):
        """Upload an image

        Provide a file and album id to upload to a given album.  Using PUT
        method as described in the API Documentation.
        http://wiki.smugmug.net/display/API/Uploading
        """
        if "File" not in kwargs or "AlbumID" not in kwargs:
            raise SmugMugException("File and AlbumID are required")

        if "FileName" not in kwargs:
            kwargs["FileName"] = os.path.basename(kwargs["File"])

        # Upload Url
        url = "http://upload.smugmug.com/%s" % quote(kwargs["FileName"])

        # Read file in binary mode
        f = open(kwargs["File"], "rb")
        data = f.read()
        f.close()

        header = {}
        header["Content-MD5"] = hashlib.md5(data).hexdigest()
        header["Content-Length"] = os.path.getsize(kwargs["File"])
        header["X-Smug-Version"] = self.api_version
        header["X-Smug-ResponseType"] = "JSON"

        if self.oauth_token:
            oauth_params = self._get_oauth_request_params(url, {}, "PUT")
            header["Authorization"] = "OAuth realm=" + \
                '"http://api.smugmug.com/", ' + \
                ", ".join('%s="%s"' % (k, urlencodeRFC3986(v)) for k, v
                                      in sorted(oauth_params.items()))
        elif self.session_id:
            header["X-Smug-SessionID"] = self.session_id
        else:
            raise SmugMugException("Authorization required for upload")

        # Other headers
        for k, v in kwargs.items():
            if k == "File":
                continue
            header["X-Smug-" + k] = v

        rsp = self._fetch_url(url, data, header, "PUT")
        return self._handle_response(rsp)

    def _make_handler(self, method):
        """API method contructor"""
        secure = False
        if (method.startswith("login_with") or
            (method.startswith("auth") and self.check_version(min="1.3.0")) or
                self.secure):
            secure = True

        method = "smugmug." + method.replace("_", ".")

        def api_request(**kwargs):
            """Fetches the given API call"""
            if secure:
                url = "https://secure.smugmug.com/services/api/json/"
            else:
                url = "http://api.smugmug.com/services/api/json/"
            url = url + self.api_version + "/"
            kwargs.update(dict(method=method))

            # Add the OAuth resource request signature if we have credentials
            if self.oauth_secret:
                all_args = {}
                all_args.update(kwargs)
                oauth = self._get_oauth_request_params(url, all_args, "POST")
                kwargs.update(oauth)
            elif self.check_version(min="1.3.0"):  # Anonymous access
                kwargs.update(dict(APIKey=self.api_key))
            elif self.check_version(max="1.2.2") and self.session_id:
                kwargs.update(dict(SessionID=self.session_id))

            rsp = self._fetch_url(url, urlencode(kwargs))

            return self._handle_response(rsp)

        return api_request

    def _handle_response(self, response):
        """API response handler that parse JSON response"""
        parsed = json.loads(compat_decode(response))

        #API response for image upload method does not return method name
        if "method" not in parsed:
            parsed["method"] = "smugmug.images.upload"

        if parsed["stat"] == "fail":
            raise SmugMugException("SmugMug API Error for method " +
                                   parsed["method"] +
                                   ": (" + str(parsed["code"]) + ") " +
                                   parsed["message"])

        return parsed

    #Oauth methods
    def authorize(self, access="Public", perm="Read"):
        """Returns the SmugMug authorization URL for the given request token"""
        return "http://api.smugmug.com/services/oauth/authorize.mg?" + \
            urlencode(dict(oauth_token=self.oauth_token)) + \
            "&Access=" + access + "&Permissions=" + perm

    def _get_oauth_request_params(self, url, parameters={}, method="GET",
                                  timestamp=None, nonce=None):
        """Returns the OAuth parameters as a dict for the resource request"""
        if timestamp is None:
            timestamp = int(time.time())
        if nonce is None:
            nonce = binascii.b2a_hex(uuid.uuid4().bytes)

        base_args = dict(
            oauth_consumer_key=self.api_key,
            oauth_signature_method="HMAC-SHA1",
            oauth_timestamp=str(timestamp),
            oauth_nonce=str(nonce),
            oauth_version="1.0",
        )
        if self.oauth_token:
            base_args["oauth_token"] = self.oauth_token
        args = {}
        args.update(base_args)
        args.update(parameters)
        signature = self._oauth_signature(method, url, args)
        base_args["oauth_signature"] = compat_decode(signature)
        return base_args

    def _oauth_signature(self, method, url, parameters={}):
        """Calculates the HMAC-SHA1 OAuth signature for the given request."""
        parts = urlparse(url)
        proto, netloc, path = parts[:3]
        normalized_url = proto.lower() + "://" + netloc.lower() + path

        base_elems = []
        base_elems.append(method.upper())
        base_elems.append(normalized_url)
        base_elems.append("&".join("%s=%s" % (k, urlencodeRFC3986(str(v)))
                                   for k, v in sorted(parameters.items())))
        base_string = "&".join(urlencodeRFC3986(e) for e in base_elems)

        key_elems = [self.oauth_secret]
        if self.oauth_token_secret:
            key_elems.append(self.oauth_token_secret)
        else:
            key_elems.append("")
        key = "&" . join(key_elems)

        hash = hmac.new(key.encode("utf-8"), base_string.encode("utf-8"),
                        hashlib.sha1)
        return binascii.b2a_base64(hash.digest())[:-1]

    def _fetch_url(self, url, body, header={}, method="POST"):
        header.update({"User-Agent": self.application})
        data = compat_encode(body)
        req = urlrequest.Request(url, data, header)
        if method == "PUT":
            req.get_method = lambda: "PUT"
        return urlopen(req).read()

    def check_version(self, min=None, max=None):
        """Checks API version

        This function validates the API version called
        against the min and max version supported.
        """
        version = self.api_version.split(".")
        if min:
            min_version = min.split(".")
            if version < min_version:
                return False
        if max:
            max_version = max.split(".")
            if version > max_version:
                return False

        return True


def urlencodeRFC3986(val):
    """URL encoder required by Oauth"""
    return quote(compat_encode(val), safe="~")


class SmugMugException(Exception):
    """SmugMug specific exception"""
    pass

if __name__ == '__main__':
    pass
