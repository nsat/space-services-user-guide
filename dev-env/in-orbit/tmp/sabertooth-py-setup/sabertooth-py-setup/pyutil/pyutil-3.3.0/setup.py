#!/usr/bin/env python
# -*- coding: utf-8; fill-column: 77 -*-
# -*- indent-tabs-mode: nil -*-

# pyutil -- utility functions and classes
#
# This file is part of pyutil; see README.rst for licensing terms.

import os, io, re, sys

import versioneer

from setuptools import find_packages, setup

trove_classifiers=[
    u"Development Status :: 5 - Production/Stable",
    u"License :: OSI Approved :: GNU General Public License (GPL)",
    u"License :: DFSG approved",
    u"Intended Audience :: Developers",
    u"Operating System :: Microsoft :: Windows",
    u"Operating System :: Unix",
    u"Operating System :: MacOS :: MacOS X",
    u"Operating System :: OS Independent",
    u"Natural Language :: English",
    u"Programming Language :: Python",
    u"Programming Language :: Python :: 2",
    u"Programming Language :: Python :: 2.7",
    u"Programming Language :: Python :: 3",
    u"Programming Language :: Python :: 3.5",
    u"Programming Language :: Python :: 3.6",
    u"Programming Language :: Python :: 3.7",
    u"Topic :: Utilities",
    u"Topic :: Software Development :: Libraries",
    ]

PKG=u'pyutil'

doc_fnames=[ u'COPYING.SPL.txt', u'COPYING.GPL', u'COPYING.TGPPL.rst', u'README.rst', u'CREDITS' ]

# In case we are building for a .deb with stdeb's sdist_dsc command, we put the
# docs in "share/doc/python-$PKG".
doc_loc = u"share/doc/" + PKG

data_files = [
    (doc_loc, doc_fnames),
    (os.path.join(u'pyutil', u'data'), [os.path.join(u'pyutil', u'data', u'wordlist.txt')])
    ]

readmetext = io.open(u'README.rst', encoding='utf-8').read()

setup(name=PKG,
      version=versioneer.get_version(),
      cmdclass=versioneer.get_cmdclass(),
      description=u'a collection of utilities for Python programmers',
      long_description=readmetext,
      long_description_content_type=u'text/x-rst',
      author=u"tpltnt",
      author_email=u'tpltnt+pyutil@nbkawtg.net',
      url=u'https://github.com/tpltnt/' + PKG,
      license=u'GNU GPL', # see README.rst for details -- there are also alternative licences
      packages=find_packages(),
      include_package_data=True,
      data_files=data_files,
      install_requires=[],
      extras_require={
          u'jsonutil': [u'simplejson >= 2.1.0',],
          u'randcookie': [u'zbase32 >= 1.0',],
          },
      tests_require=[
          u'twisted >= 15.5.0',  # for trial (eg user: test_observer)
          u'mock >= 1.3.0',
      ],
      classifiers=trove_classifiers,
      entry_points = {
          u'console_scripts': [
              u'randcookie = pyutil.scripts.randcookie:main',
              u'tailx = pyutil.scripts.tailx:main',
              u'lines = pyutil.scripts.lines:main',
              u'randfile = pyutil.scripts.randfile:main',
              u'unsort = pyutil.scripts.unsort:main',
              u'verinfo = pyutil.scripts.verinfo:main',
              u'try_decoding = pyutil.scripts.try_decoding:main',
              u'passphrase = pyutil.scripts.passphrase:main',
              ] },
      test_suite=PKG+u".test",
      zip_safe=False, # I prefer unzipped for easier access.
      )
