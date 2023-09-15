# -*- coding: utf-8 -*-
"""
Unittests

Verify that DataMatrix class works as expected. Note that most testing is
done in the codec-specific tests. This file is for the rest.

.. author: Adrian Schlatter
"""

import ppf.datamatrix as put
import unittest
import random
from .common import EDIFACT, ASCII


class Test_DataMatrix_Attributes(unittest.TestCase):
    """Test DataMatrix attribute acces for unexpected exceptions"""

    def setUp(self):
        try:
            self.dm = put.DataMatrix(EDIFACT)
        except:
            self.fail('Exception upon valid instantiation')

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


class Test_DataMatrix_Invalid_Codec(unittest.TestCase):
    """Test DataMatrix"""

    def test_invalid_codec(self):
        """Verify that exception is raised for invalid codec"""

        with self.assertRaises(TypeError):
            put.DataMatrix('message', codecs=['invalid_codec'])


class Test_A(unittest.TestCase):
    """Test simple edifact datamatrix."""

    def test_square_matrix(self):
        dm = put.DataMatrix('A', rect=False)
        truth = [[1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
                 [1, 1, 0, 1, 1, 0, 0, 0, 1, 1],
                 [1, 0, 0, 0, 1, 1, 0, 1, 0, 0],
                 [1, 0, 0, 1, 1, 0, 1, 0, 1, 1],
                 [1, 0, 0, 1, 0, 1, 0, 0, 0, 0],
                 [1, 0, 0, 1, 0, 0, 1, 0, 1, 1],
                 [1, 1, 0, 1, 0, 0, 1, 1, 0, 0],
                 [1, 1, 0, 0, 1, 1, 1, 1, 0, 1],
                 [1, 1, 0, 0, 0, 0, 1, 0, 0, 0],
                 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
        self.assertEqual(dm.matrix, truth)

    def test_rect_matrix(self):
        """Test that rectangular matrix is not square."""
        dm = put.DataMatrix('~', rect=True)
        truth = [[1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
                 [1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1],
                 [1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0],
                 [1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1],
                 [1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, 1, 1, 0],
                 [1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 1],
                 [1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0],
                 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
        self.assertTrue(dm.matrix, truth)


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
