#!/usr/bin/env python
# -*- coding: utf-8-with-signature-unix; fill-column: 77 -*-
# -*- indent-tabs-mode: nil -*-

#  This file is part of pyutil; see README.rst for licensing terms.

import unittest

from pyutil.assertutil import _assert
from pyutil import strutil

class Teststrutil(unittest.TestCase):
    def test_short_input(self):
        self.assertTrue(strutil.pop_trailing_newlines("\r\n") == "")
        self.assertTrue(strutil.pop_trailing_newlines("\r") == "")
        self.assertTrue(strutil.pop_trailing_newlines("x\r\n") == "x")
        self.assertTrue(strutil.pop_trailing_newlines("x\r") == "x")

    def test_split(self):
        _assert(strutil.split_on_newlines("x\r\ny") == ["x", "y",], strutil.split_on_newlines("x\r\ny"))
        _assert(strutil.split_on_newlines("x\r\ny\r\n") == ["x", "y", '',], strutil.split_on_newlines("x\r\ny\r\n"))
        _assert(strutil.split_on_newlines("x\n\ny\n\n") == ["x", '', "y", '', '',], strutil.split_on_newlines("x\n\ny\n\n"))

    def test_commonprefix(self):
        _assert(strutil.commonprefix(["foo","foobarooo", "foosplat",]) == 'foo', strutil.commonprefix(["foo","foobarooo", "foosplat",]))
        _assert(strutil.commonprefix(["foo","afoobarooo", "foosplat",]) == '', strutil.commonprefix(["foo","afoobarooo", "foosplat",]))

    def test_commonsuffix(self):
        _assert(strutil.commonsuffix(["foo","foobarooo", "foosplat",]) == '', strutil.commonsuffix(["foo","foobarooo", "foosplat",]))
        _assert(strutil.commonsuffix(["foo","foobarooo", "foosplato",]) == 'o', strutil.commonsuffix(["foo","foobarooo", "foosplato",]))
        _assert(strutil.commonsuffix(["foo","foobarooofoo", "foosplatofoo",]) == 'foo', strutil.commonsuffix(["foo","foobarooofoo", "foosplatofoo",]))
