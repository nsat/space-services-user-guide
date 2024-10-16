# -*- coding: utf-8; fill-column: 77 -*-
# -*- indent-tabs-mode: nil -*-
from unittest import TestCase

from pyutil import jsonutil as json

class TestDefault(TestCase):
    def test_default(self):
        self.assertEqual(
            json.dumps(type, default=repr),
            json.dumps(repr(type)))
