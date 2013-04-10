Smugpy [![Build Status](https://secure.travis-ci.org/chrishoffman/smugpy.png?branch=master)](http://travis-ci.org/chrishoffman/smugpy) [![Coverage Status](https://coveralls.io/repos/chrishoffman/smugpy/badge.png?branch=master)](https://coveralls.io/r/chrishoffman/smugpy)
======

Smugpy is an Python 2.x/3.x library for the [SmugMug](https://secure.smugmug.com/signup.mg?Coupon=2TqKwSOXw5HeU) API created by Chris Hoffman.  Smugpy supports all versions of the API and Oauth 1.0 for API versions 1.2.2+.  This library also works in [Google App Engine](http://code.google.com/appengine/).  For more information on the SmugMug API, see [SmugMug API Documentation](http://wiki.smugmug.net/display/API/).

Installation
------------

The latest **stable version** of smugpy can always be installed via [pip](http://www.pip-installer.org/en/latest/index.html):
    
    pip install -U smugpy

Or, you can install the **development version** directly from GitHub:

    pip install -U https://github.com/chrishoffman/smugpy/tarball/master

Or, download the package and install manually:

    python setup.py install

Usage
-----
Simple request (1.3.0+):

```python
from smugpy import SmugMug

API_KEY = "XXXXXXXXXXXXXXXXXXXXXXXXX"

smugmug = SmugMug(api_key=API_KEY, api_version="1.3.0", app_name="TestApp")
albums = smugmug.albums_get(NickName="williams")

for album in albums["Albums"]:
    print "%s, %s" % (album["id"], album["Title"])
```
For more examples, see the [examples](https://github.com/chrishoffman/smugpy/tree/master/examples) directory.

Helping Out
-----------
If you notice any problems, please report them to the GitHub issue tracker at [https://github.com/chrishoffman/smugpy/issues](http://github.com/chrishoffman/smugpy/issues). 

License
-------
Smugpy is released under the MIT license.
