#!/usr/bin/env python
# -*- coding: utf-8-with-signature-unix; fill-column: 77 -*-
# -*- indent-tabs-mode: nil -*-

#  This file is part of pyutil; see README.rst for licensing terms.

from __future__ import print_function
import os

try:
    from twisted.trial import unittest
except ImportError as le:
    print("Skipping %s since it requires Twisted and Twisted could not be imported: %s" % (__name__, le,))
else:
    from pyutil import PickleSaver, fileutil

    class Thingie(PickleSaver.PickleSaver):
        def __init__(self, fname, delay=30):
            PickleSaver.PickleSaver.__init__(self, fname=fname, attrs={'tmp_store':'False'}, DELAY=delay)

    class PickleSaverTest(unittest.TestCase):
        def _test_save_now(self, fname):
            thingie = Thingie(fname, delay=0)
            thingie.tmp_store = 'True'
            thingie.lazy_save() # Note: it was constructed with default save delay of 0.

        def test_save_now(self):
            """
            This test should create a lazy save object, save it with no delay and check if the file exists.
            """
            tempdir = fileutil.NamedTemporaryDirectory()

            fname = os.path.join(tempdir.name, "picklesavertest")
            self._test_save_now(fname)
            self.assertTrue(os.path.isfile(fname), "The file [%s] does not exist." %(fname,))

            tempdir.shutdown()
