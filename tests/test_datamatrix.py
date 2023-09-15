# -*- coding: utf-8 -*-
"""
Unittests

Verify that DataMatrix class works as expected. Note that most testing is
done in the codec-specific tests. This file is for the rest.

.. author: Adrian Schlatter
"""

import unittest
import ppf.datamatrix as put


class Test_DataMatrix(unittest.TestCase):
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
