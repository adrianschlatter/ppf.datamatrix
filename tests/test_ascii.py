# -*- coding: utf-8 -*-
"""
Unittests

Verify that datamatrix.ascii codec works as expected

.. author: Adrian Schlatter
"""

import unittest
import ppf.datamatrix as put
from .common import ASCII


class Test_datamatrix_ascii(unittest.TestCase):
    """Test codecs datamatrix.ascii."""

    def test_consistency(self):
        """Verify that coding + decoding return the original message."""
        for i in range(128):
            if 2 * i > len(ASCII):
                msg = ASCII[i:] + ASCII[:3 * i - len(ASCII)]
            else:
                msg = ASCII[i:2 * i]

            code = msg.encode('datamatrix.ascii')
            decoded = code.decode('datamatrix.ascii')
            self.assertEqual(decoded, msg)

    def test_encode_known(self):
        """Encode and verify correctness."""
        code = 'A'.encode('datamatrix.ascii')
        self.assertEqual(code, b'B')

    def test_encode_digitpair(self):
        """Encode a pair of digits and verify correctness."""
        code = '60'.encode('datamatrix.ascii')
        self.assertEqual(code, bytes([130 + 60]))

    def test_encode_digittriplet(self):
        """Encode a group of 3 digits and verify correctness."""
        code = '325'.encode('datamatrix.ascii')
        self.assertEqual(code, bytes([130 + 32, ord('5') + 1]))

    def test_encode_to_datamatrix(self):
        """Verify that encoding to datamatrix works."""
        for i in range(len(ASCII)):
            if 2 * i > len(ASCII):
                msg = ASCII[i:] + ASCII[:3 * i - len(ASCII)]
            else:
                msg = ASCII[i:2 * i]

            # assert that this does not raise:
            datamatrix = put.DataMatrix(msg)

            self.assertTrue(len(datamatrix.matrix) > 0)

    def test_encode_to_rect_datamatrix(self):
        """Verify that encoding to datamatrix works."""
        for i in range(len(ASCII)):
            if 2 * i > len(ASCII):
                msg = ASCII[i:] + ASCII[:3 * i - len(ASCII)]
            else:
                msg = ASCII[i:2 * i]

            # assert that this does not raise:
            datamatrix = put.DataMatrix(msg, rect=True)

            self.assertTrue(len(datamatrix.matrix) > 0)


if __name__ == '__main__':
    # This enables running the unit tests by running this script which is
    # much more convenient than 'python setup.py test' while developing tests.
    # Note: package-under-test needs to be in python-path
    unittest.main()
