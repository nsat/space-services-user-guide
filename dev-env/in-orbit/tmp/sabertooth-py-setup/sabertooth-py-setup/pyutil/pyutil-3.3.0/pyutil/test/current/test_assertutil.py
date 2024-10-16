#!/usr/bin/env python
# -*- coding: utf-8-with-signature-unix; fill-column: 77 -*-
# -*- indent-tabs-mode: nil -*-

#  This file is part of pyutil; see README.rst for licensing terms.

# Python Standard Library modules
import sys, unittest

from pyutil import assertutil

class AssertUtilTestCase(unittest.TestCase):
    def test_bad_precond(self):
        adict=23
        try:
            assertutil.precondition(isinstance(adict, dict), "adict is required to be a dict.", 23, adict=adict, foo=None)
        except AssertionError as le:
            if sys.version_info[0] == 2:
                self.assertEqual(le.args[0], "precondition: 'adict is required to be a dict.' <type 'str'>, 23 <type 'int'>, 'adict': 23 <type 'int'>, 'foo': None <type 'NoneType'>")
            else:
                self.assertEqual(le.args[0], "precondition: 'adict is required to be a dict.' <class 'str'>, 23 <class 'int'>, 'adict': 23 <class 'int'>, 'foo': None <class 'NoneType'>")
