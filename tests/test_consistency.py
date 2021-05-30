# -*- coding: utf-8 -*-
"""
Unittests

Verify that our datamatrices are consistent with
https://raw.githubusercontent.com/datalog/datamatrix-svg/master/datamatrix.js

.. author: Adrian Schlatter
"""

import unittest
import ppf.datamatrix as put


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


if __name__ == '__main__':
    # This enables running the unit tests by running this script which is
    # much more convenient than 'python setup.py test' while developing tests.
    # Note: package-under-test needs to be in python-path
    unittest.main()
