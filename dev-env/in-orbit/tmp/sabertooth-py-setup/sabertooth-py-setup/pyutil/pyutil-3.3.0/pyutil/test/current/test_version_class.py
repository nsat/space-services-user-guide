# -*- coding: utf-8; fill-column: 77 -*-
# -*- indent-tabs-mode: nil -*-

#  This file is part of pyutil; see README.rst for licensing terms.

import unittest

from pyutil import version_class

V = version_class.Version

class T(unittest.TestCase):
    def test_rc_regex_rejects_rc_suffix(self):
        self.assertRaises(ValueError, V, '9.9.9rc9')

    def test_rc_regex_rejects_trailing_garbage(self):
        self.assertRaises(ValueError, V, '9.9.9c9HEYTHISISNTRIGHT')

    def test_comparisons(self):
        self.assertTrue(V('1.0') < V('1.1'))
        self.assertTrue(V('1.0a1') < V('1.0'))
        self.assertTrue(V('1.0a1') < V('1.0b1'))
        self.assertTrue(V('1.0b1') < V('1.0c1'))
        self.assertTrue(V('1.0a1') < V('1.0a1-r99'))
        self.assertEqual(V('1.0a1.post987'), V('1.0a1-r987'))
        self.assertEqual(str(V('1.0a1.post999')), '1.0.0a1-r999')
        self.assertEqual(str(V('1.0a1-r999')), '1.0.0a1-r999')
        self.assertNotEqual(V('1.0a1'), V('1.0a1-r987'))
