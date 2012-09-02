from distutils.core import setup
import sys
from textwrap import dedent

install_requires = []
if sys.version_info < (2, 6):
    install_requires.append("simplejson")

setup(
    name = "smugpy",
    version = "0.3.1",
    description = "SmugMug Python API",
    author = "Chris Hoffman",
    author_email = "chris@chrishoffman.org",
    license = "MIT",
    url = "http://github.com/chrishoffman/smugpy/",
    platforms = ["any"],
    packages = ["smugpy"],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    install_requires = install_requires,
    long_description = dedent("""\
        The SmugMug API lets to you access your albums, photos, and videos,
        and much more.  See http://wiki.smugmug.net/display/API/ for more information.
        
        Example::
        
            from smugpy import SmugMug
            
            API_KEY = "XXXXXXXXXXXXXXXXXXXXXXXXX"
            
            smugmug = SmugMug(api_key=API_KEY, app_name="TestApp")
            smugmug.login_anonymously()
            albums = smugmug.albums_get(NickName="williams")
            
            for album in albums["Albums"]:
                print "%s, %s" % (album["id"], album["Title"])
    """)
)
