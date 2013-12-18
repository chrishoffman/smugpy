#!/usr/bin/env python

from __future__ import print_function
from smugpy import SmugMug
import sys

#Aliasing for differences in Python 2.x and 3.x
if sys.version_info < (3,):
    get_input = raw_input
else:
    get_input = input

API_KEY = "XXXXXXXXXXXXXXXXXXXXXXXXX"
OAUTH_SECRET = "YYYYYYYYYYYYYYYYYYYYYYY" # From SmugMug Settings -> Discovery -> API Keys
APP_NAME="TestApp"

# Request a "request token" from the smugmug servers for the given permissions.
#
# Return a pair (url, requestToken) that can be used to authorize this app to
# access the account of whomever logs in at the URL.
def smugmugOauthRequestToken(access="Public", perm="Read"):
    smugmug = SmugMug(api_key=API_KEY, oauth_secret=OAUTH_SECRET, app_name=APP_NAME)

    # Get a token that is short-lived (probably about 5 minutes) and can be used
    # only to setup authorization at SmugMug
    response = smugmug.auth_getRequestToken()

    # Get the URL that the user must visit to authorize this app (implicilty includes the request token in the URL)
    url = smugmug.authorize(access=access, perm=perm)

    return url, response['Auth'] # (should contain a 'Token')

# "Visit" the URL (well, print the instructions the user should use to visit
# the URL).  Once this is done the request token can be used to log in to
# that user's account and get an "access token" for this app to use that
# account.
#
# This implementation blocks until the user acknowledges that they've completed
# the authorization at smugmug.com
def userAuthorizeAtSmugmug(url):
    get_input("Authorize app at %s\n\nPress Enter when complete.\n" % (url))

# Request an "access token" based on the given request token.  The request token
# should be authorized at smugmug.com.
#
# Return the "access token" that encodes the user's identity and the secrets
# that authorize this app to access that user's smugmug account.
def smugmugOauthGetAccessToken(requestToken):
    # Use the request token to log in (which should be authorized now)
    smugmug = SmugMug(api_key=API_KEY, oauth_secret=OAUTH_SECRET,
                      oauth_token=requestToken['Token']['id'],
                      oauth_token_secret=requestToken['Token']['Secret'],
                      app_name=APP_NAME)
 
    # The request token is good for 1 operation: to get an access token.
    response = smugmug.auth_getAccessToken()

    # The access token should be good until the user explicitly
    # disables it at smugmug.com in their settings panel.
    return response['Auth'];


# Log into smugmug.com with an authorized accessToken.  The accessToken includes
# the user's identity and, effectively, a password to get this application into
# the account.
def smugmugOauthUseAccessToken(accessToken):
    # Use the access token to log in
    smugmug = SmugMug(api_key=API_KEY, oauth_secret=OAUTH_SECRET,
                      oauth_token=accessToken['Token']['id'],
                      oauth_token_secret=accessToken['Token']['Secret'],
                      app_name=APP_NAME)
    return smugmug;

###
### Main
###

# Step 1: get request token and authorization URL:
(url, requestToken) = smugmugOauthRequestToken()

# Step 2: "visit" the authorization URL:
userAuthorizeAtSmugmug(url)

# Step 3: Upgrade the authorized request token into an access token
accessToken = smugmugOauthGetAccessToken(requestToken)

# Step 3.5: You should save off the accessToken so you can resume at
# the following step from now on.  There is no need to jump through
# the request token and authorization URL more than once.

# Step 4 (and step 1 in the future): log in with the (saved) access
# token to get an authorized connection to smugmug.com:

smugmug = smugmugOauthUseAccessToken(accessToken)

albums = smugmug.albums_get(NickName=accessToken['User']['NickName'])
for album in albums["Albums"]:
    print("%s, %s" % (album["id"], album["Title"]))
