# -*- coding: utf-8 -*-
"""
Unittests

Verify that datamatrix.text codec works as expected

.. author: Adrian Schlatter
"""

import ppf.datamatrix
import unittest
from .common import ASCII, Codec_Test


class Test_datamatrix_text(Codec_Test, unittest.TestCase):
    """Test codecs datamatrix.text."""

    CODEC = 'datamatrix.text'
    ALPHABET = ASCII
    # Apparently, datamatrix-svg has a problem with '`' (it encodes
    # 'A`' to the same as it encode 'A9'). Verified ppf.datamatrix against
    # datamatrix-svg without '`' => OK
    # ALPHABET_ENC below is what I belief to be the correct encoding of the
    # ALPHABET:
    ALPHABET_ENC = (
            b'\xef\x00\x01\x06C\x00y\x19\x06\x00\xf1+\xc9\x01i>\x8c\x01'
            b'\xe1QO\x02Yd\x12\x02\xd1v\xd5\x03I\x89\x98\x03\xc1\x9c[\x04'
            b'9\xaf\x1e\x04\xb1\xc2:\x00*\x06\x92\x12\xed\x07\n%\xb0\x07'
            b'\x828s\x07\xfaK6\x08u 83sF\xae\x08\x9ad:\t\x12v\xfd\t\x8b'
            b'\x06\x93\x0c\xfb\x19V\rs,\x19\r\xeb>\xdc\x0ecQ\x9f\x0e\xdbd'
            b'b\x0fSw%\x0f\xcb\x89\xe8\x10C\x9c\xab\t\xb2\x90\x01\n*\xa2'
            b'\xd1Y\xe9m$\x80_\x93\x9a\xa6\xd5\xba\x10\xcdK\xe0\x86\xf3\x9b'
            b'\xa9-\x11\x0b\xbb\xf0\xfe')
    KNOWN_PAIR = {'msg': 'A', 'enc': b'B'}
    CODEC_MODULE_NAME = 'codec_text'

    def test_encode_known_long(self):
        """
        Encode long string and verify correctness.

        'long' means: Long enough to have word packing.
        """
        code = (9 * 'a' + '!').encode('datamatrix.text')
        self.assertEqual(code, b'\xefY\xbfY\xbfY\xbf\xfe"')

    def test_return_to_ascii(self):
        """Encode string that results in lonely RTA code at the end"""
        code = 'Hello World!'.encode('datamatrix.text')
        self.assertEqual(code, b'\xef\r\xd3\xa0E\x13(\xb3\xf2ji\xfe')


if __name__ == '__main__':
    # This enables running the unit tests by running this script which is
    # much more convenient than 'python setup.py test' while developing tests.
    # Note: package-under-test needs to be in python-path
    unittest.main()
