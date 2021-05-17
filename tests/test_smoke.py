# -*- coding: utf-8 -*-
"""
Unittests

.. author: Adrian Schlatter
"""

import unittest
import ppf.datamatrix as put

# Datamatrix has the following encodings:
# TEXT, C40, X12, EDIFACT, BASE256
# TEXT and C40 both encode the entire ASCII character table (in a
# different way).
# X12 and EDIFACT are subsets of ASCII characters.
# BASE256 is the (binary) 8-bit alphabet.
ASCII = ''.join([chr(i) for i in range(128)])
X12 = '\r*> 01234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ'
EDIFACT = ''.join([chr(i) for i in range(32, 95)])
BASE256 = bytes(range(256))


class Smoke_Test(object):
    """Template class to test for unexpected exceptions."""

    def setUp(self):
        """Implement in Child class to setUp instance of your class."""
        pass

    def test_methods(self):
        """Run each method and test for exceptions."""
        methods = ['svg', '__repr__', '_repr_svg_']

        for method in methods:
            try:
                getattr(self.dm, method)()
            except:     # noqa: E722
                self.fail(f'DataMatrix.{method} raises exception')

    def test_properties(self):
        """Access each property and test for exceptions."""
        props = ['message', 'ascii', 'edifact', 'matrix']

        for prop in props:
            try:
                getattr(self.dm, prop)
            except:     # noqa: E722
                self.fail(f'DataMatrix.{prop} raises exception')


class Test_EDIFACT(Smoke_Test, unittest.TestCase):
    """Smoke test EDIFACT DataMatrix."""

    def setUp(self):
        try:
            self.dm = put.DataMatrix(EDIFACT)
        except:     # noqa: E722
            self.fail('Exception upon valid instantiation')


class Test_ASCII(Smoke_Test, unittest.TestCase):
    """Smoke test ASCII DataMatrix."""

    def setUp(self):
        try:
            self.dm = put.DataMatrix(ASCII)
        except:     # noqa: E722
            self.fail('Exception upon valid instantiation')


@unittest.skip('Not implemented yet')
class Test_BASE256(Smoke_Test, unittest.TestCase):
    """Smoke test BASE256 DataMatrix."""

    def setUp(self):
        try:
            self.dm = put.DataMatrix(BASE256)
        except:     # noqa: E722
            self.fail('Exception upon valid instantiation')


if __name__ == '__main__':
    # This enables running the unit tests by running this script which is
    # much more convenient than 'python setup.py test' while developing tests.
    # Note: package-under-test needs to be in python-path
    unittest.main()
