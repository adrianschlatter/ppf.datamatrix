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

# output of ppf.datamatrix.DataMatrix('T').svg() as of v0.2:
# (if we deviate from this, we break backward compatibility)
svg_line_of_T_v0_2_0 = (
    '<?xml version="1.0" encoding="utf-8" ?>'
    '<svg baseProfile="tiny" version="1.2" height="12px" width="12px" '
    'style="background-color:#FFF" xmlns="http://www.w3.org/2000/svg" '
    'xmlns:ev="http://www.w3.org/2001/xml-events" '
    'xmlns:xlink="http://www.w3.org/1999/xlink">'
    '<path d="M1,1.5 h1m1,0h1m1,0h1m1,0h1m1,0h1m1,0m-10,1h2m1,0h2m2,0h3m-10,'
    '1h1m3,0h3m1,0h1m1,0m-10,1h1m2,0h4m1,0h2m-10,1h1m7,0h1m1,0m-10,1h2m3,'
    '0h1m1,0h1m1,0h1m-10,1h1m2,0h3m4,0m-10,1h1m3,0h3m2,0h1m-10,1h3m5,0h1m1,'
    '0m-10,1h10m-10,1" stroke="#000" stroke-width="1"/>'
    '</svg>')

svg_rect_of_T = (
    '<?xml version="1.0" encoding="utf-8"?>'
    '<svg baseProfile="tiny" version="1.2" viewBox="-1 -1 12 12" '
    'width="12mm" height="12mm" style="background-color:#FFF" '
    'xmlns="http://www.w3.org/2000/svg" '
    'xmlns:ev="http://www.w3.org/2001/xml-events" '
    'xmlns:xlink="http://www.w3.org/1999/xlink">\n'
    '<rect width="1" height="1" x="0" y="0" fill="#000"/>\n'
    '<rect width="1" height="1" x="2" y="0" fill="#000"/>\n'
    '<rect width="1" height="1" x="4" y="0" fill="#000"/>\n'
    '<rect width="1" height="1" x="6" y="0" fill="#000"/>\n'
    '<rect width="1" height="1" x="8" y="0" fill="#000"/>\n'
    '<rect width="1" height="1" x="0" y="1" fill="#000"/>\n'
    '<rect width="1" height="1" x="1" y="1" fill="#000"/>\n'
    '<rect width="1" height="1" x="3" y="1" fill="#000"/>\n'
    '<rect width="1" height="1" x="4" y="1" fill="#000"/>\n'
    '<rect width="1" height="1" x="7" y="1" fill="#000"/>\n'
    '<rect width="1" height="1" x="8" y="1" fill="#000"/>\n'
    '<rect width="1" height="1" x="9" y="1" fill="#000"/>\n'
    '<rect width="1" height="1" x="0" y="2" fill="#000"/>\n'
    '<rect width="1" height="1" x="4" y="2" fill="#000"/>\n'
    '<rect width="1" height="1" x="5" y="2" fill="#000"/>\n'
    '<rect width="1" height="1" x="6" y="2" fill="#000"/>\n'
    '<rect width="1" height="1" x="8" y="2" fill="#000"/>\n'
    '<rect width="1" height="1" x="0" y="3" fill="#000"/>\n'
    '<rect width="1" height="1" x="3" y="3" fill="#000"/>\n'
    '<rect width="1" height="1" x="4" y="3" fill="#000"/>\n'
    '<rect width="1" height="1" x="5" y="3" fill="#000"/>\n'
    '<rect width="1" height="1" x="6" y="3" fill="#000"/>\n'
    '<rect width="1" height="1" x="8" y="3" fill="#000"/>\n'
    '<rect width="1" height="1" x="9" y="3" fill="#000"/>\n'
    '<rect width="1" height="1" x="0" y="4" fill="#000"/>\n'
    '<rect width="1" height="1" x="8" y="4" fill="#000"/>\n'
    '<rect width="1" height="1" x="0" y="5" fill="#000"/>\n'
    '<rect width="1" height="1" x="1" y="5" fill="#000"/>\n'
    '<rect width="1" height="1" x="5" y="5" fill="#000"/>\n'
    '<rect width="1" height="1" x="7" y="5" fill="#000"/>\n'
    '<rect width="1" height="1" x="9" y="5" fill="#000"/>\n'
    '<rect width="1" height="1" x="0" y="6" fill="#000"/>\n'
    '<rect width="1" height="1" x="3" y="6" fill="#000"/>\n'
    '<rect width="1" height="1" x="4" y="6" fill="#000"/>\n'
    '<rect width="1" height="1" x="5" y="6" fill="#000"/>\n'
    '<rect width="1" height="1" x="0" y="7" fill="#000"/>\n'
    '<rect width="1" height="1" x="4" y="7" fill="#000"/>\n'
    '<rect width="1" height="1" x="5" y="7" fill="#000"/>\n'
    '<rect width="1" height="1" x="6" y="7" fill="#000"/>\n'
    '<rect width="1" height="1" x="9" y="7" fill="#000"/>\n'
    '<rect width="1" height="1" x="0" y="8" fill="#000"/>\n'
    '<rect width="1" height="1" x="1" y="8" fill="#000"/>\n'
    '<rect width="1" height="1" x="2" y="8" fill="#000"/>\n'
    '<rect width="1" height="1" x="8" y="8" fill="#000"/>\n'
    '<rect width="1" height="1" x="0" y="9" fill="#000"/>\n'
    '<rect width="1" height="1" x="1" y="9" fill="#000"/>\n'
    '<rect width="1" height="1" x="2" y="9" fill="#000"/>\n'
    '<rect width="1" height="1" x="3" y="9" fill="#000"/>\n'
    '<rect width="1" height="1" x="4" y="9" fill="#000"/>\n'
    '<rect width="1" height="1" x="5" y="9" fill="#000"/>\n'
    '<rect width="1" height="1" x="6" y="9" fill="#000"/>\n'
    '<rect width="1" height="1" x="7" y="9" fill="#000"/>\n'
    '<rect width="1" height="1" x="8" y="9" fill="#000"/>\n'
    '<rect width="1" height="1" x="9" y="9" fill="#000"/>\n'
    '</svg>')


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


class Test_SVGOutput(unittest.TestCase):
    """Test SVG output of DataMatrix."""

    def test_geom_invalid(self):
        """Raise NotImplementedError for invalid geom."""
        dm = put.DataMatrix('T')

        with self.assertRaises(NotImplementedError):
            dm.svg(geom='invalid')

    def test_geom_equal_default_v0_2_0(self):
        """Backward compatibility: Test against the SVG output of v0.2.0."""
        dm = put.DataMatrix('T')
        self.assertTrue(len(dm.matrix) == 10)
        self.assertEqual(dm.svg(), svg_line_of_T_v0_2_0)

    def test_geom_equal_rect(self):
        """Test geom='rect'"""
        dm = put.DataMatrix('T')
        self.assertTrue(len(dm.matrix) == 10)
        self.assertEqual(dm.svg(geom='rect'), svg_rect_of_T)


if __name__ == '__main__':
    # This enables running the unit tests by running this script which is
    # much more convenient than 'python setup.py test' while developing tests.
    # Note: package-under-test needs to be in python-path
    unittest.main()
