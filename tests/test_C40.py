# -*- coding: utf-8 -*-
"""
Unittests

Verify that datamatrix.C40 codec works as expected

.. author: Adrian Schlatter
"""

import unittest
from .common import ASCII
import ppf.datamatrix as pu


class Test_datamatrix_C40(unittest.TestCase):
    """Test codecs datamatrix.C40."""

    def test_consistency(self):
        """Verify that coding + decoding return the original message."""
        for i in range(128):
            if 2 * i > len(ASCII):
                msg = ASCII[i:] + ASCII[:3 * i - len(ASCII)]
            else:
                msg = ASCII[i:2 * i]

            code = msg.encode('datamatrix.C40')
            decoded = code.decode('datamatrix.C40')
            self.assertEqual(decoded, msg)

    def test_encode_known_short(self):
        """
        Encode short string and verify correctness.

        'short' means: Too short to pack a single word.
        """
        code = 'A'.encode('datamatrix.C40')
        self.assertEqual(code, b'B')

    def test_encode_known_long(self):
        """
        Encode long string and verify correctness.

        'long' means: Long enough to have word packing.
        """
        code = (9 * 'A' + '!').encode('datamatrix.C40')
        self.assertEqual(code, b'\xe6Y\xbfY\xbfY\xbf\xfe"')

    def test_encode_ASCII(self):
        """Encode ASCII and compare to datamatrix-svg."""
        code = ASCII.encode('datamatrix.C40')
        truth = (b'\xe6\x00\x01\x06C\x00y\x19\x06\x00\xf1+\xc9\x01i>\x8c\x01'
                 b'\xe1QO\x02Yd\x12\x02\xd1v\xd5\x03I\x89\x98\x03\xc1\x9c[\x04'
                 b'9\xaf\x1e\x04\xb1\xc2:\x00*\x06\x92\x12\xed\x07\n%\xb0\x07'
                 b'\x828s\x07\xfaK6\x08u 83sF\xae\x08\x9ad:\t\x12v\xfd\t\x97`'
                 b'Rs\x8d\x86\xc8\x9a\x03\xad>\xc0y\xd3\xb4\xe6\xef\xf3\xff\t'
                 b'\xda\x96B\nS\x00R\x0c\xd3\x13\x15\rK%\xd8\r\xc38\x9b\x0e;K^'
                 b'\x0e\xb3^!\x0f+p\xe4\x0f\xa3\x83\xa7\x10\x1b\x96j\x10\x93'
                 b'\xa9-\x11\x0b\xbb\xf0\xfe')
        # Note: truth's last code is \xfe which means 'return to ascii'.
        # We do not consider it as an error if code is equal to truth
        # except for missing an 0xFE at the end:
        self.assertTrue(code == truth or code == truth[:-1])

    def test_decode_invalid_C40(self):
        """Try to decode invalid code."""

        code = 9 * b'\x00'
        with self.assertRaises(ValueError):
            code.decode('datamatrix.C40')

    def test_search_nonTEXT(self):
        """Test that search_codec callback returns None for non-C40."""

        from ppf.datamatrix import codec_C40
        self.assertTrue(codec_C40.search_codec_C40('invalid') is None)


if __name__ == '__main__':
    # This enables running the unit tests by running this script which is
    # much more convenient than 'python setup.py test' while developing tests.
    # Note: package-under-test needs to be in python-path
    unittest.main()
