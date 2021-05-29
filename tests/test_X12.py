# -*- coding: utf-8 -*-
"""
Unittests

Verify that datamatrix.X12 codec works as expected

.. author: Adrian Schlatter
"""

import unittest
from .common import X12
import ppf.datamatrix as pu


class Test_datamatrix_X12(unittest.TestCase):
    """Test codecs datamatrix.X12."""

    def test_consistency(self):
        """Verify that coding + decoding return the original message."""
        for i in range(len(X12)):
            if 2 * i > len(X12):
                msg = X12[i:] + X12[:3 * i - len(X12)]
            else:
                msg = X12[i:2 * i]

            code = msg.encode('datamatrix.X12')
            decoded = code.decode('datamatrix.X12')
            self.assertEqual(decoded, msg)

    def test_encode_known(self):
        """Encode and verify correctness."""
        code = 'A'.encode('datamatrix.X12')
        self.assertEqual(code, b'\xEE\xFEB')

    def test_encode_X12(self):
        """Encode entire alphabet and compare to datamatrix-svg."""
        # Ooops, datamatrix-svg fails at '>'. Test without '>'
        X12_ = '\r* 01234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        code = X12_.encode('datamatrix.X12')
        self.assertEqual(code, b'\xee\x00,\x19\xcf-\n@EQ\xef`Rs\x8d\x86\xc8'
                         b'\x9a\x03\xad>\xc0y\xd3\xb4\xe6\xef\xfe[')


if __name__ == '__main__':
    # This enables running the unit tests by running this script which is
    # much more convenient than 'python setup.py test' while developing tests.
    # Note: package-under-test needs to be in python-path
    unittest.main()
