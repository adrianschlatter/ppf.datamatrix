# -*- coding: utf-8 -*-
"""
Unittests

Things shared between unittests are defined here to keep code DRY.

.. author: Adrian Schlatter
"""

# Datamatrix has the following encodings:
# TEXT, C40, X12, EDIFACT, BASE256
# TEXT and C40 both encode the entire ASCII character table (in a
# different way).
# X12 and EDIFACT are subsets of ASCII characters.
# BASE256 is the (binary) 8-bit alphabet.

ASCII = bytes(range(128)).decode('ascii')
EDIFACT = bytes(range(32, 95)).decode('ascii')
X12 = '\r*> 01234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ'
BASE256 = bytes(range(256))
