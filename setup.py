#!/usr/bin/env python

from setuptools import setup, find_packages
from textwrap import dedent
import sys

install_requires = []
if sys.version_info < (2, 6):
    install_requires.append("simplejson")

setup(
    name = "smugpy",
    version = "0.3.0-pre",
    description = "SmugMug Python API",
    author = "Chris Hoffman",
    author_email = "chris@chrishoffman.org",
    license = "MIT",
    url = "http://github.com/chrishoffman/smugpy/",
    platforms = ["any"],
    packages = find_packages(exclude=("tests",)),
    install_requires = install_requires,
    long_description = dedent("""\
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
    """)
)
