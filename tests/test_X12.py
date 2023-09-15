# -*- coding: utf-8 -*-
"""
Unittests

Verify that datamatrix.X12 codec works as expected

.. author: Adrian Schlatter
"""

import ppf.datamatrix
import unittest
from .common import X12, Codec_Test


class Test_datamatrix_X12(Codec_Test, unittest.TestCase):
    """Test codecs datamatrix.X12."""

    CODEC = 'datamatrix.X12'
    ALPHABET = X12
    # NOTED: datamatrix-svg *fails* at '>'! => Let datamatrix-svg encode:
    # X12_ = '\r* 01234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    # => ppf.datamatrix passed test. Then, encoded full X12 with this
    # ppf.datamatrix => ALPHABET_ENC:
    ALPHABET_ENC = (
            b'\xee\x00+\x13f&\xa19\xdcM\rY\xe9m$\x80_\x93\x9a\xa6\xd5\xba'
            b'\x10\xcdK\xe0\x86\xfeZ[')
    KNOWN_PAIR = {'msg': 'A', 'enc': b'B'}
    CODEC_MODULE_NAME = 'codec_X12'

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


if __name__ == '__main__':
    # This enables running the unit tests by running this script which is
    # much more convenient than 'python setup.py test' while developing tests.
    # Note: package-under-test needs to be in python-path
    unittest.main()
