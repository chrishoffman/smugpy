#!/usr/bin/env python

from smugpy import SmugMug

API_KEY = "XXXXXXXXXXXXXXXXXXXXXXXXX"

smugmug = SmugMug(api_key=API_KEY, app_name="TestApp")
smugmug.login_anonymously()
albums = smugmug.albums_get(NickName="williams") # Moon River Photography, thanks Andy!

for album in albums["Albums"]:
    print "%s, %s" % (album["id"], album["Title"])