#!/usr/bin/env python
# -*- coding: utf-8-with-signature-unix; fill-column: 77 -*-
# -*- indent-tabs-mode: nil -*-

#  This file is part of pyutil; see README.rst for licensing terms.

import unittest

from pyutil import mathutil
from pyutil.assertutil import _assert

class MathUtilTestCase(unittest.TestCase):
    def _help_test_is_power_of_k(self, k):
        for i in range(2, 40):
            _assert(mathutil.is_power_of_k(k**i, k), k, i)

    def test_is_power_of_k(self):
        for i in range(2, 5):
            self._help_test_is_power_of_k(i)

    def test_log_ceil(self):
        f = mathutil.log_ceil
        self.assertEqual(f(1, 2), 0)
        self.assertEqual(f(1, 3), 0)
        self.assertEqual(f(2, 2), 1)
        self.assertEqual(f(2, 3), 1)
        self.assertEqual(f(3, 2), 2)

    def test_log_floor(self):
        f = mathutil.log_floor
        self.assertEqual(f(1, 2), 0)
        self.assertEqual(f(1, 3), 0)
        self.assertEqual(f(2, 2), 1)
        self.assertEqual(f(2, 3), 0)
        self.assertEqual(f(3, 2), 1)

    def test_div_ceil(self):
        f = mathutil.div_ceil
        self.assertEqual(f(0, 1), 0)
        self.assertEqual(f(0, 2), 0)
        self.assertEqual(f(0, 3), 0)
        self.assertEqual(f(1, 3), 1)
        self.assertEqual(f(2, 3), 1)
        self.assertEqual(f(3, 3), 1)
        self.assertEqual(f(4, 3), 2)
        self.assertEqual(f(5, 3), 2)
        self.assertEqual(f(6, 3), 2)
        self.assertEqual(f(7, 3), 3)
        self.assertTrue(isinstance(f(0.0, 1), int))
        self.assertEqual(f(7.0, 3.0), 3)
        self.assertEqual(f(7, 3.0), 3)
        self.assertEqual(f(7.0, 3), 3)
        self.assertEqual(f(6.0, 3.0), 2)
        self.assertEqual(f(6.0, 3), 2)
        self.assertEqual(f(6, 3.0), 2)

    def test_next_multiple(self):
        f = mathutil.next_multiple
        self.assertEqual(f(5, 1), 5)
        self.assertEqual(f(5, 2), 6)
        self.assertEqual(f(5, 3), 6)
        self.assertEqual(f(5, 4), 8)
        self.assertEqual(f(5, 5), 5)
        self.assertEqual(f(5, 6), 6)
        self.assertEqual(f(32, 1), 32)
        self.assertEqual(f(32, 2), 32)
        self.assertEqual(f(32, 3), 33)
        self.assertEqual(f(32, 4), 32)
        self.assertEqual(f(32, 5), 35)
        self.assertEqual(f(32, 6), 36)
        self.assertEqual(f(32, 7), 35)
        self.assertEqual(f(32, 8), 32)
        self.assertEqual(f(32, 9), 36)
        self.assertEqual(f(32, 10), 40)
        self.assertEqual(f(32, 11), 33)
        self.assertEqual(f(32, 12), 36)
        self.assertEqual(f(32, 13), 39)
        self.assertEqual(f(32, 14), 42)
        self.assertEqual(f(32, 15), 45)
        self.assertEqual(f(32, 16), 32)
        self.assertEqual(f(32, 17), 34)
        self.assertEqual(f(32, 18), 36)
        self.assertEqual(f(32, 589), 589)

    def test_pad_size(self):
        f = mathutil.pad_size
        self.assertEqual(f(0, 4), 0)
        self.assertEqual(f(1, 4), 3)
        self.assertEqual(f(2, 4), 2)
        self.assertEqual(f(3, 4), 1)
        self.assertEqual(f(4, 4), 0)
        self.assertEqual(f(5, 4), 3)

    def test_is_power_of_k_part_2(self):
        f = mathutil.is_power_of_k
        for i in range(1, 100):
            if i in (1, 2, 4, 8, 16, 32, 64):
                self.assertTrue(f(i, 2), "but %d *is* a power of 2" % i)
            else:
                self.assertFalse(f(i, 2), "but %d is *not* a power of 2" % i)
        for i in range(1, 100):
            if i in (1, 3, 9, 27, 81):
                self.assertTrue(f(i, 3), "but %d *is* a power of 3" % i)
            else:
                self.assertFalse(f(i, 3), "but %d is *not* a power of 3" % i)

    def test_next_power_of_k(self):
        f = mathutil.next_power_of_k
        self.assertEqual(f(0,2), 1)
        self.assertEqual(f(1,2), 1)
        self.assertEqual(f(2,2), 2)
        self.assertEqual(f(3,2), 4)
        self.assertEqual(f(4,2), 4)
        for i in range(5, 8): self.assertEqual(f(i,2), 8, "%d" % i)
        for i in range(9, 16): self.assertEqual(f(i,2), 16, "%d" % i)
        for i in range(17, 32): self.assertEqual(f(i,2), 32, "%d" % i)
        for i in range(33, 64): self.assertEqual(f(i,2), 64, "%d" % i)
        for i in range(65, 100): self.assertEqual(f(i,2), 128, "%d" % i)

        self.assertEqual(f(0,3), 1)
        self.assertEqual(f(1,3), 1)
        self.assertEqual(f(2,3), 3)
        self.assertEqual(f(3,3), 3)
        for i in range(4, 9): self.assertEqual(f(i,3), 9, "%d" % i)
        for i in range(10, 27): self.assertEqual(f(i,3), 27, "%d" % i)
        for i in range(28, 81): self.assertEqual(f(i,3), 81, "%d" % i)
        for i in range(82, 200): self.assertEqual(f(i,3), 243, "%d" % i)

    def test_ave(self):
        f = mathutil.ave
        self.assertEqual(f([1,2,3]), 2)
        self.assertEqual(f([0,0,0,4]), 1)
        self.assertAlmostEqual(f([0.0, 1.0, 1.0]), .666666666666)

    def assertEqualContents(self, a, b):
        self.assertEqual(sorted(a), sorted(b))

    def test_permute(self):
        f = mathutil.permute
        self.assertEqualContents(f([]), [])
        self.assertEqualContents(f([1]), [[1]])
        self.assertEqualContents(f([1,2]), [[1,2], [2,1]])
        self.assertEqualContents(f([1,2,3]),
                                     [[1,2,3], [1,3,2],
                                      [2,1,3], [2,3,1],
                                      [3,1,2], [3,2,1]])
