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
OAUTH_SECRET = "YYYYYYYYYYYYYYYYYYYYYYY"

smugmug = SmugMug(api_key=API_KEY, oauth_secret=OAUTH_SECRET, app_name="TestApp")

#Oauth handshake
smugmug.auth_getRequestToken()
get_input("Authorize app at %s\n\nPress Enter when complete.\n" % (smugmug.authorize()))   
smugmug.auth_getAccessToken()

albums = smugmug.albums_get(NickName="williams") # Moon River Photography, thanks Andy!
for album in albums["Albums"]:
    print("%s, %s" % (album["id"], album["Title"]))
