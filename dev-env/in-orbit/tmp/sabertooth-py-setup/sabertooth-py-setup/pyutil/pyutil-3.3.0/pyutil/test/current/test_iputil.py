#!/usr/bin/env python
# -*- coding: utf-8-with-signature-unix; fill-column: 77 -*-
# -*- indent-tabs-mode: nil -*-

#  This file is part of pyutil; see README.rst for licensing terms.

from __future__ import print_function

try:
    from twisted.trial import unittest
    unittest # http://divmod.org/trac/ticket/1499
except ImportError as le:
    print("Skipping test_iputil since it requires Twisted and Twisted could not be imported: %s" % (le,))
else:
    from pyutil import iputil, testutil
    import re

    DOTTED_QUAD_RE=re.compile("^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$")

    class ListAddresses(testutil.SignalMixin):
        def test_get_local_ip_for(self):
            addr = iputil.get_local_ip_for('127.0.0.1')
            self.assertTrue(DOTTED_QUAD_RE.match(addr))

        def test_list_async(self):
            try:
                from twisted.trial import unittest
                unittest # http://divmod.org/trac/ticket/1499
                from pyutil import iputil
            except ImportError as le:
                raise unittest.SkipTest("iputil could not be imported (probably because its dependency, Twisted, is not installed).  %s" % (le,))

            d = iputil.get_local_addresses_async()
            def _check(addresses):
                self.assertTrue(len(addresses) >= 1) # always have localhost
                self.assertTrue("127.0.0.1" in addresses, addresses)
            d.addCallbacks(_check)
            return d
        test_list_async.timeout=2
