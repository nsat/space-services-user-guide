# -*- coding: utf-8; fill-column: 77 -*-
# -*- indent-tabs-mode: nil -*-

#  This file is part of pyutil; see README.rst for licensing terms.

"""
extended version number class
"""

# verlib a.k.a. distutils.version by Tarek Ziadé.
from pyutil.verlib import NormalizedVersion

# Python Standard Library
import functools, re

# End users see version strings like this:

# "1.0.0"
#  ^ ^ ^
#  | | |
#  | | '- micro version number
#  | '- minor version number
#  '- major version number

# The first number is "major version number".  The second number is the "minor
# version number" -- it gets bumped whenever we make a new release that adds or
# changes functionality.  The third version is the "micro version number" -- it
# gets bumped whenever we make a new release that doesn't add or change
# functionality, but just fixes bugs (including performance issues).

# Early-adopter end users see version strings like this:

# "1.0.0a1"
#  ^ ^ ^^^
#  | | |||
#  | | ||'- release number
#  | | |'- a=alpha, b=beta, c=release candidate, or none
#  | | '- micro version number
#  | '- minor version number
#  '- major version number

# The optional "a" or "b" stands for "alpha release" or "beta release"
# respectively.  The number after "a" or "b" gets bumped every time we
# make a new alpha or beta release. This has the same form and the same
# meaning as version numbers of releases of Python.

# Developers see "full version strings", like this:

# "1.0.0a1-55"
#  ^ ^ ^^^  ^
#  | | |||  |
#  | | |||  '- nano version number
#  | | ||'- release number
#  | | |'- a=alpha, b=beta, c=release candidate or none
#  | | '- micro version number
#  | '- minor version number
#  '- major version number

# or else like this:

# "1.0.0a1-r22155"
#  ^ ^ ^^^  ^
#  | | |||  |
#  | | |||  '- revision number
#  | | ||'- release number
#  | | |'- a=alpha, b=beta, c=release candidate or none
#  | | '- micro version number
#  | '- minor version number
#  '- major version number

# The presence of the nano version number means that this is a development
# version.  There are no guarantees about compatibility, etc.  This version is
# considered to be more recent than the version without this field
# (e.g. "1.0.0a1").

# The nano version number or revision number is meaningful only to developers.
# It gets generated automatically from darcs revision control history by
# "darcsver.py".  The nano version number is the count of patches that have been
# applied since the last version number tag was applied.  The revision number is
# the count of all patches that have been applied in the history.

VERSION_BASE_RE_STR="(\d+)(\.(\d+)(\.(\d+))?)?((a|b|c)(\d+))?(\.dev(\d+))?"
VERSION_SUFFIX_RE_STR="(-(\d+|r\d+)|.post\d+)?"
VERSION_RE_STR=VERSION_BASE_RE_STR + VERSION_SUFFIX_RE_STR
VERSION_RE=re.compile("^" + VERSION_RE_STR + "$")

@functools.total_ordering
class Version(object):
    def __init__(self, vstring=None):
        self.major = None
        self.minor = None
        self.micro = None
        self.prereleasetag = None
        self.prerelease = None
        self.nano = None
        self.revision = None
        if vstring:
            try:
                self.parse(vstring)
            except ValueError as le:
                le.args = tuple(le.args + ('vstring:', vstring,))
                raise

    def parse(self, vstring):
        mo = VERSION_RE.search(vstring)
        if not mo:
            raise ValueError("Not a valid version string for pyutil.version_class.Version(): %r" % (vstring,))

        self.major = int(mo.group(1))
        self.minor = mo.group(3) and int(mo.group(3)) or 0
        self.micro = mo.group(5) and int(mo.group(5)) or 0
        reltag = mo.group(6)
        if reltag:
            reltagnum = int(mo.group(8))
            self.prereleasetag = mo.group(7)
            self.prerelease = reltagnum

        if mo.group(11):
            if mo.group(11)[0] == '-':
                if mo.group(12)[0] == 'r':
                    self.revision = int(mo.group(12)[1:])
                else:
                    self.nano = int(mo.group(12))
            else:
                assert mo.group(11).startswith('.post'), mo.group(11)
                self.revision = int(mo.group(11)[5:])

        # XXX in the future, to be compatible with the Python "rational version numbering" scheme, we should move to using .post$REV instead of -r$REV:
        # self.fullstr = "%d.%d.%d%s%s" % (self.major, self.minor, self.micro, self.prereleasetag and "%s%d" % (self.prereleasetag, self.prerelease,) or "", self.nano and "-%d" % (self.nano,) or self.revision and ".post%d" % (self.revision,) or "",)
        self.fullstr = "%d.%d.%d%s%s" % (self.major, self.minor, self.micro, self.prereleasetag and "%s%d" % (self.prereleasetag, self.prerelease,) or "", self.nano and "-%d" % (self.nano,) or self.revision and "-r%d" % (self.revision,) or "",)

    def user_str(self):
        return self.full_str()

    def full_str(self):
        if hasattr(self, 'fullstr'):
            return self.fullstr
        else:
            return 'None'

    def __str__(self):
        return self.full_str()

    def __repr__(self):
        return self.__str__()

    def __cmp__ (self, other):
        return cmp(NormalizedVersion(str(self)), NormalizedVersion(str(other)))

    def __eq__ (self, other):
        return NormalizedVersion(str(self)) == NormalizedVersion(str(other))

    def __lt__ (self, other):
        return NormalizedVersion(str(self)) < NormalizedVersion(str(other))
