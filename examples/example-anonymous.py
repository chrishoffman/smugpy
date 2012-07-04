#!/usr/bin/env python

from __future__ import print_function
from smugpy import SmugMug

API_KEY = "XXXXXXXXXXXXXXXXXXXXXXXXX"

smugmug = SmugMug(api_key=API_KEY, api_version="1.2.2", app_name="TestApp")
smugmug.login_anonymously()
albums = smugmug.albums_get(NickName="williams") # Moon River Photography, thanks Andy!

for album in albums["Albums"]:
    print("%s, %s" % (album["id"], album["Title"]))
