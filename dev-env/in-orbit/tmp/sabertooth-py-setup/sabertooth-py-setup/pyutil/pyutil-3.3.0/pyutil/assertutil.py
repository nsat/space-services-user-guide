# -*- coding: utf-8; fill-column: 77 -*-
# -*- indent-tabs-mode: nil -*-

#  This file is part of pyutil; see README.rst for licensing terms.

"""
Tests useful in assertion checking, prints out nicely formated messages too.
"""

from .humanreadable import hr

def _format_error(prefix, args, kwargs):
    if prefix:
        msgbuf=[prefix]
        if args or kwargs:
            msgbuf.append(": ")
    else:
        msgbuf=[]
    if args:
        msgbuf.append(", ".join(["%s %s" % tuple(map(hr, (arg, type(arg),))) for arg in args]))
    if kwargs:
        if args:
            msgbuf.append(", ")
        msgbuf.append(", ".join(["%s: %s %s" % tuple(map(hr, (k, kwargs[k], type(kwargs[k]),))) for k in sorted(kwargs.keys())]))
    return "".join(msgbuf)

def _assert(___cond=False, *args, **kwargs):
    if ___cond:
        return True
    raise AssertionError(_format_error(None, args, kwargs))

def precondition(___cond=False, *args, **kwargs):
    if ___cond:
        return True
    raise AssertionError(_format_error("precondition", args, kwargs))

def postcondition(___cond=False, *args, **kwargs):
    if ___cond:
        return True
    raise AssertionError(_format_error("postcondition", args, kwargs))
