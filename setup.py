#!/usr/bin/env python

from distutils.core import setup

setup(
    name = "smugpy",
    version = "0.2",
    description = "SmugMug Python API",
    author = "Chris Hoffman",
    author_email = "chris@chrishoffman.org",
    url = "http://github.com/chrishoffman/smugpy/",
    package_dir = {"": "src"},
    py_modules = ["smugpy"],
    keywords = ["smugmug"],
    long_description = """\
    Python SmugMug Helper Library
    ----------------------------

    DESCRIPTION
    The SmugMug API lets to you access your albums, photos, and videos,
    and much more.  See http://wiki.smugmug.net/display/API/ for more information.

    USAGE
    To use the Smugpy library, just 'import smugpy' in the your current py
    file. As shown in example-anonymous.py, you will need to specify the API_KEY
    given to you by SmugMug before you can make API requests. See 
    http://wiki.smugmug.net/display/API/ for more information.

    LICENSE 
    The SmugMug Python Helper Library is distributed under the MIT License 
    """
)