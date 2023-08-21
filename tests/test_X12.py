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

    def test_encode_known_short(self):
        """
        Encode short string and verify correctness.

        'short' means: Too short to pack a single word.
        """
        code = 'A'.encode('datamatrix.X12')
        self.assertEqual(code, b'B')

    def test_encode_known_long(self):
        """
        Encode long string and verify correctness.

        'long' means: Long enough to have word packing.
        """
        code = (8 * 'A' + '*').encode('datamatrix.X12')
        self.assertEqual(code, b'\xeeY\xbfY\xbfY\xb2\xfe')

    def test_encode_X12(self):
        """Encode entire alphabet and compare to datamatrix-svg."""
        # Ooops, datamatrix-svg fails at '>'. Test without '>'
        X12_ = '\r* 01234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        code = X12_.encode('datamatrix.X12')
        self.assertEqual(code, b'\xee\x00,\x19\xcf-\n@EQ\xef`Rs\x8d\x86\xc8'
                         b'\x9a\x03\xad>\xc0y\xd3\xb4\xe6\xef\xfe[')

    def test_decode_invalid_X12(self):
        """Try to decode invalid code."""

        code = 9 * b'\x00'
        with self.assertRaises(ValueError):
            code.decode('datamatrix.X12')

    def test_search_nonX12(self):
        """Test that search_codec callback returns None for non-X12."""

        from ppf.datamatrix import codec_X12
        self.assertTrue(codec_X12.search_codec_X12('invalid') is None)


if __name__ == '__main__':
    # This enables running the unit tests by running this script which is
    # much more convenient than 'python setup.py test' while developing tests.
    # Note: package-under-test needs to be in python-path
    unittest.main()
