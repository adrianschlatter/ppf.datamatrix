# -*- coding: utf-8 -*-
"""
Unittests

Verify that datamatrix.edifact codec works as expected

.. author: Adrian Schlatter
"""

import unittest
import ppf.datamatrix as put

EDIFACT = bytes(range(32, 95)).decode('ascii')


class Test_datamatrix_edifact(unittest.TestCase):
    """Test codecs datamatrix.edifact."""

    def test_encode_decode(self):
        """Verify that coding + decoding return the original message."""
        for i in range(len(EDIFACT)):
            if 2 * i > len(EDIFACT):
                msg = EDIFACT[i:] + EDIFACT[:3 * i - len(EDIFACT)]
            else:
                msg = EDIFACT[i:2 * i]

            code = msg.encode('datamatrix.edifact')
            decoded = code.decode('datamatrix.edifact')
            self.assertEqual(decoded, msg)

    def test_raises(self):
        """Verify that error is raised for invalid EDIFACT."""
        code = bytes([0])
        with self.assertRaises(ValueError):
            code.decode('datamatrix.edifact')

    def test_encode_to_square_datamatrix(self):
        """Verify that encoding to square datamatrix works."""
        for i in range(len(EDIFACT)):
            if 2 * i > len(EDIFACT):
                msg = EDIFACT[i:] + EDIFACT[:3 * i - len(EDIFACT)]
            else:
                msg = EDIFACT[i:2 * i]

            # assert that this does not raise:
            datamatrix = put.DataMatrix(msg)

            self.assertTrue(len(datamatrix.matrix) > 0)

    def test_encode_to_rect_datamatrix(self):
        """Verify that encoding to rectangular datamatrix works."""
        for i in range(len(EDIFACT)):
            if 2 * i > len(EDIFACT):
                msg = EDIFACT[i:] + EDIFACT[:3 * i - len(EDIFACT)]
            else:
                msg = EDIFACT[i:2 * i]

            # assert that this does not raise:
            datamatrix = put.DataMatrix(msg, rct=True)

            m = datamatrix.matrix
            self.assertTrue(len(m) > 0)

    def test_encode_known(self):
        """Encode and verify correctness."""
        code = 'A'.encode('datamatrix.edifact')
        self.assertEqual(code, b'\xf0\x1fB')


if __name__ == '__main__':
    # This enables running the unit tests by running this script which is
    # much more convenient than 'python setup.py test' while developing tests.
    # Note: package-under-test needs to be in python-path
    unittest.main()
