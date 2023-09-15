# -*- coding: utf-8 -*-
"""
Unittests

Verify that datamatrix.ascii codec works as expected

.. author: Adrian Schlatter
"""

import ppf.datamatrix
import unittest
from .common import ASCII, Codec_Test


class Test_datamatrix_ascii(Codec_Test, unittest.TestCase):
    """Test codecs datamatrix.ascii."""

    CODEC = 'datamatrix.ascii'
    ALPHABET = ASCII
    ALPHABET_ENC = (
            b'\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f\x10\x11'
            b'\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f !"#$%&'
            b'\'()*+,-./0\x83\x99\xaf\xc5\xdb;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ'
            b'[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~\x7f\x80')
    KNOWN_PAIR = {'msg': 'A', 'enc': b'B'}
    CODEC_MODULE_NAME = 'codec_ascii'

    def test_encode_digitpair(self):
        """Encode a pair of digits and verify correctness."""
        code = '60'.encode('datamatrix.ascii')
        self.assertEqual(code, bytes([130 + 60]))

    def test_encode_digittriplet(self):
        """Encode a group of 3 digits and verify correctness."""
        code = '325'.encode('datamatrix.ascii')
        self.assertEqual(code, bytes([130 + 32, ord('5') + 1]))


if __name__ == '__main__':
    # This enables running the unit tests by running this script which is
    # much more convenient than 'python setup.py test' while developing tests.
    # Note: package-under-test needs to be in python-path
    unittest.main()
