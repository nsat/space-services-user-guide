# -*- coding: utf-8; fill-column: 77 -*-
# -*- indent-tabs-mode: nil -*-
import math
from unittest import TestCase

from pyutil import jsonutil as json

class TestFloat(TestCase):
    def test_floats(self):
        for num in [1617161771.7650001, math.pi, math.pi**100, math.pi**-100]:
            self.assertEqual(float(json.dumps(num)), num)
