#!/usr/bin/env python
"""
This file contains parameters for mhealthx to fill settings in setup.py,
the mhealthx top-level docstring, and for building the docs.
In setup.py we execute this file, so it cannot import mindboggle.
"""

# mhealthx version information.  An empty _version_extra corresponds to a
# full release.  '.dev' as a _version_extra string means a development version
_version_major = 1
_version_minor = 0
_version_micro = 0
_version_extra = ''

# Format expected by setup.py and doc/source/conf.py: string of form "X.Y.Z"
__version__ = "{0}.{1}.{2}{3}".format(_version_major,
                                      _version_minor,
                                      _version_micro,
                                      _version_extra)

CLASSIFIERS = ["Development Status :: 3 - Alpha",
               "Environment :: Console",
               "Intended Audience :: Science/Research",
               "License :: OSI Approved :: Apache v2.0",
               "Operating System :: Linux",
               "Programming Language :: Python 3",
               "Topic :: Scientific/Engineering"]

description  = "Automated feature extraction from sensor data"

# Note: this long_description is actually a copy/paste from the top-level
# README.rst, so that it shows up nicely on PyPI.  So please remember to edit
# it only in one place and sync it correctly.
long_description = """
==========
Mindboggle
==========

mhealthx is a software package for automated feature extraction
intended for analyzing mobile health sensor data,
licensed under the terms of the Apache v2.0 license.
Current information can always be found at the mhealthx website,
https://binarybottle.github.io/mhealthx, and on the Github main repository,
http://github.com/binarybottle/mhealthx

"""

# Main setup parameters
NAME                = 'mhealthx'
MAINTAINER          = "Arno Klein"
MAINTAINER_EMAIL    = "arno@childmind.org"
DESCRIPTION         = description
LONG_DESCRIPTION    = long_description
URL                 = "https://binarybottle.github.io/mhealthx"
DOWNLOAD_URL        = "https://binarybottle.github.io/mhealthx"
LICENSE             = "Apache v2.0"
CLASSIFIERS         = CLASSIFIERS
AUTHOR              = "Arno Klein"
AUTHOR_EMAIL        = "arno@childmind.org"
PLATFORMS           = "Linux"
MAJOR               = _version_major
MINOR               = _version_minor
MICRO               = _version_micro
ISRELEASE           = _version_extra
VERSION             = __version__
PROVIDES            = ["mhealthx"]
#REQUIRES            = ["numpy (>={0})".format(NUMPY_MIN_VERSION)]

