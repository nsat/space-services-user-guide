#!/usr/bin/env python
# -*- coding: utf-8-with-signature-unix; fill-column: 77 -*-
# -*- indent-tabs-mode: nil -*-

#  This file is part of pyutil; see README.rst for licensing terms.

import unittest

from pyutil.xor import xor

# unit tests
def _help_test(xf):
    assert xf(b'\000', b'\000') == b'\000'
    assert xf(b'\001', b'\000') == b'\001'
    assert xf(b'\001', b'\001') == b'\000'
    assert xf(b'\000\001', b'\000\001') == b'\000\000'
    assert xf(b'\100\101', b'\000\101') == b'\100\000'

class Testy(unittest.TestCase):
    def test_em(self):
        for xorfunc in (xor.py_xor, xor.py_xor_simple, xor.xor,):
            if callable(xorfunc):
                # print "testing xorfunc ", xorfunc
                _help_test(xorfunc)
