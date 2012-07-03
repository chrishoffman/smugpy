"""
Example of how to change a setting on multiple albums.

Finds a set of albums (in this example, the match is based on Category name)
and changes an attribute (in this example, the 'Public' property is examined and changed).

Written by Jeff Dean, 16-June-2012
Uses smugpy by Chris Hoffman: https://github.com/chrishoffman/smugpy

This example finds all albums in the 'Sports' category and shows how to
display and change the 'Public' attribute.

Uses the old SmugMug API (1.2.2) because it's not worth the effort of using
new style authentication (OAuth) for a one-shot script.

You will need to obtain an API Key from SmugMug to use this script:
    http://www.smugmug.com/hack/apikeys

Example of information for a single album (returned by albums_get):

{u'Category': {u'Name': u'Events', u'id': 11},
 u'Key': u'xyzzy',
 u'SubCategory': {u'Name': u'Holidays', u'id': 987654},
 u'Title': u'2000-01-01 New Years Eve Party',
 u'id': 1234567}    

"""
import smugpy
import getpass

SCRIPT_NAME = '<enter your script name here>'
API_KEY = '<enter your API key here>'

CATEGORY = 'Sports'

# using the old API (1.2.2), which is easier to use for one shot scripts (avoids OAuth)
smugmug = smugpy.SmugMug(api_key=API_KEY, api_version="1.2.2", app_name=SCRIPT_NAME)

# signon
USER_NAME = raw_input('Email address: ')
PASSWORD = getpass.getpass('Password: ')
smugmug.login_withPassword(EmailAddress=USER_NAME, Password=PASSWORD)

# Get all albums
albums = smugmug.albums_get()

# find just matching albums
matches = [x for x in albums['Albums'] if x['Category']['Name'] == CATEGORY]

# display the matching albums
for album in matches:
    info = smugmug.albums_getInfo(AlbumID=album['id'], AlbumKey=album['Key'])
    print "%s - %s" % (info['Album']['Public'], album['Title'])

# uncomment the code below to change all matching albums
#
## THIS OPERATION WILL CHANGE THE ATTRIBUTES OF ALL MATCHING ALBUMS.
## USE WITH CAUTION!
#
#for album in matches
#	smugmug.albums_changeSettings(AlbumID=album['id'], Public='False')
