# -*- coding: utf-8 -*-
"""
Unittests

.. author: Adrian Schlatter
"""

import unittest
import random
from .common import ASCII, EDIFACT, BASE256
import ppf.datamatrix as put


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
            except:
                self.fail(f'DataMatrix.{method} raises exception')

    def test_properties(self):
        """Access each property and test for exceptions."""
        props = ['message', 'matrix']

        for prop in props:
            try:
                getattr(self.dm, prop)
            except:
                self.fail(f'DataMatrix.{prop} raises exception')


class Test_EDIFACT(Smoke_Test, unittest.TestCase):
    """Smoke test EDIFACT DataMatrix."""

    def setUp(self):
        try:
            self.dm = put.DataMatrix(EDIFACT)
        except:
            self.fail('Exception upon valid instantiation')


class Test_ASCII(Smoke_Test, unittest.TestCase):
    """Smoke test ASCII DataMatrix."""

    def setUp(self):
        try:
            self.dm = put.DataMatrix(ASCII)
        except:
            self.fail('Exception upon valid instantiation')


@unittest.skip('Not implemented yet')
class Test_BASE256(Smoke_Test, unittest.TestCase):
    """Smoke test BASE256 DataMatrix."""

    def setUp(self):
        try:
            self.dm = put.DataMatrix(BASE256)
        except:
            self.fail('Exception upon valid instantiation')


class Test_CornerCases(unittest.TestCase):
    """Test corner cases such as rarely used branches etc."""

    def test_corner_B_omit_upper_left_loop_exit(self):
        """Test said branch of code to avoid endless loop."""
        msg = ')*+,-./01'
        # make sure that this does not go into endless loop:
        datamatrix = put.DataMatrix(msg)
        self.assertTrue(len(datamatrix.matrix) > 0)

    def test_l_greater_255_blocks(self):
        """Test branch l>255 #blocks in DataMatrix.matrix property."""
        datamatrix = put.DataMatrix('A' * 230)
        self.assertTrue(len(datamatrix.matrix) > 0)

    def test_long_square_message(self):
        """Test very long messages for same behavior as datamatrix-svg."""
        m = put.DataMatrix('~' * 1558).matrix
        self.assertTrue(len(m) > 0)
        with self.assertRaises(ValueError):
            m = put.DataMatrix('~' * 1559).matrix

    def test_long_rect_message(self):
        """Test very long rect messages for same behavior as datamatrix-svg."""
        m = put.DataMatrix('~' * 49, rect=True).matrix
        self.assertTrue(len(m) < len(m[0]))

        m = put.DataMatrix('~' * 50, rect=True).matrix
        self.assertTrue(len(m) == len(m[0]))

    @unittest.skip
    def test_random_messages(self):
        """Test random messages."""
        while True:
            n = random.randint(0, 1024)
            msg = ''.join(random.choices(ASCII, k=n))
            datamatrix = put.DataMatrix(msg)
            self.assertTrue(len(datamatrix.matrix) > 0)


if __name__ == '__main__':
    # This enables running the unit tests by running this script which is
    # much more convenient than 'python setup.py test' while developing tests.
    # Note: package-under-test needs to be in python-path
    unittest.main()
