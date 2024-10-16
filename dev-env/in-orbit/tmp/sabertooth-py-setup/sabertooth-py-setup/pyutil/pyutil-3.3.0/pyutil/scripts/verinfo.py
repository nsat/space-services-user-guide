#!/usr/bin/env python
# -*- coding: utf-8-with-signature-unix; fill-column: 77 -*-
# -*- indent-tabs-mode: nil -*-
from __future__ import print_function
import exceptions
class UsageError(exceptions.Exception): pass

import sys
import pkg_resources

def main():
    if len(sys.argv) <= 1:
        raise UsageError("USAGE: verinfo DISTRIBUTIONNAME [PACKAGENAME]")
    DISTNAME=sys.argv[1]
    if len(sys.argv) >= 3:
        PACKNAME=sys.argv[2]
    else:
        PACKNAME=DISTNAME
    print("pkg_resources.require('%s') => " % (DISTNAME,))
    print(pkg_resources.require(DISTNAME))
    print("import %s;print %s => " % (PACKNAME, PACKNAME,))
    x = __import__(PACKNAME)
    print(x)
    print("import %s;print %s.__version__ => " % (PACKNAME, PACKNAME,))
    print(hasattr(x, '__version__') and x.__version__)

if __name__ == "__main__":
    main()
