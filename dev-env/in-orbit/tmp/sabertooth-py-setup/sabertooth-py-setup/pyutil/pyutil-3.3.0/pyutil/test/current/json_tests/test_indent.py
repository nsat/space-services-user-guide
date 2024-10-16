# -*- coding: utf-8; fill-column: 77 -*-
# -*- indent-tabs-mode: nil -*-
from unittest import TestCase

from pyutil import jsonutil as json
import textwrap

class TestIndent(TestCase):
    def test_indent(self):
        h = [['blorpie'], ['whoops'], [], 'd-shtaeou', 'd-nthiouh', 'i-vhbjkhnth',
             {'nifty': 87}, {'field': 'yes', 'morefield': False} ]

        expect = textwrap.dedent("""\
        [
          [
            "blorpie"
          ],
          [
            "whoops"
          ],
          [],
          "d-shtaeou",
          "d-nthiouh",
          "i-vhbjkhnth",
          {
            "nifty": 87
          },
          {
            "field": "yes",
            "morefield": false
          }
        ]""")


        d1 = json.dumps(h)
        d2 = json.dumps(h, indent=2, sort_keys=True, separators=(',', ': '))

        h1 = json.loads(d1)
        h2 = json.loads(d2)

        self.assertEqual(h1, h)
        self.assertEqual(h2, h)
        self.assertEqual(d2, expect)
