#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
.. author: Adrian Schlatter
"""

import sys


def export(obj):
    """
    Decorator that adds obj to __all__
    """

    mod = sys.modules[obj.__module__]
    mod.__all__ = getattr(mod, '__all__', []) + [obj.__name__]

    return obj
