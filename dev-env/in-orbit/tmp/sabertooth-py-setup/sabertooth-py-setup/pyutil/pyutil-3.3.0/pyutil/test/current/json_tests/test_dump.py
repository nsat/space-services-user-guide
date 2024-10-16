# -*- coding: utf-8; fill-column: 77 -*-
# -*- indent-tabs-mode: nil -*-
from unittest import TestCase
try:
    from cStringIO import StringIO
except ImportError:
    from io import StringIO

from pyutil import jsonutil as json

class TestDump(TestCase):
    def test_dump(self):
        sio = StringIO()
        json.dump({}, sio)
        self.assertEqual(sio.getvalue(), '{}')

    def test_dumps(self):
        self.assertEqual(json.dumps({}), '{}')
