#!/usr/bin/env python

from smugpy import SmugMug

API_KEY = "XXXXXXXXXXXXXXXXXXXXXXXXX"
OAUTH_SECRET = "YYYYYYYYYYYYYYYYYYYYYYY"

smugmug = SmugMug(api_key=API_KEY, oauth_secret=OAUTH_SECRET, app_name="TestApp")

#Oauth handshake
smugmug.auth_getRequestToken()
raw_input("Authorize app at %s\n\nPress Enter when complete.\n" % (smugmug.authorize()))   
smugmug.auth_getAccessToken()

albums = smugmug.albums_get(NickName="williams") # Moon River Photography, thanks Andy!
for album in albums["Albums"]:
    print "%s, %s" % (album["id"], album["Title"])