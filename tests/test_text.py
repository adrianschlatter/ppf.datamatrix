# -*- coding: utf-8 -*-
"""
Unittests

Verify that datamatrix.text codec works as expected

.. author: Adrian Schlatter
"""

import unittest
from .common import ASCII
import ppf.datamatrix as put


class Test_datamatrix_text(unittest.TestCase):
    """Test codecs datamatrix.text."""

    def test_consistency(self):
        """Verify that coding + decoding return the original message."""
        for i in range(128):
            if 2 * i > len(ASCII):
                msg = ASCII[i:] + ASCII[:3 * i - len(ASCII)]
            else:
                msg = ASCII[i:2 * i]

            code = msg.encode('datamatrix.text')
            decoded = code.decode('datamatrix.text')
            self.assertEqual(decoded, msg)

    def test_encode_known_short(self):
        """
        Encode short string and verify correctness.

        'short' means: Too short to pack a single word.
        """
        code = 'A'.encode('datamatrix.text')
        self.assertEqual(code, b'B')

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

    def test_encode_ASCII(self):
        """Encode ASCII and compare to datamatrix-svg."""
        # Apparently, datamatrix-svg has a problem with '`' (it encodes
        # 'A`' to the same as it encode 'A9'). Skip '`' for now:
        msg = ASCII[:96] + ASCII[97:]
        code = msg.encode('datamatrix.text')
        # Note: datamatrix-svg actually encodes ending in '1\xfe\x80',
        # not '3\xfe\x80'. But the '3' encodes a dummy 'set1' code, while
        # '1' encodes a dummy 'set3' code which is equivalent. "Dummy"
        # meaning immediately followed by another swich alphabet code
        # (in this case \xFE which means 'return to ascii').
        truth = (b'\xef\x00\x01\x06C\x00y\x19\x06\x00\xf1+\xc9\x01i>\x8c\x01'
                 b'\xe1QO\x02Yd\x12\x02\xd1v\xd5\x03I\x89\x98\x03\xc1\x9c[\x04'
                 b'9\xaf\x1e\x04\xb1\xc2:\x00*\x06\x92\x12\xed\x07\n%\xb0\x07'
                 b'\x828s\x07\xfaK6\x08u 83sF\xae\x08\x9ad:\t\x12v\xfd\t\x8b'
                 b'\x06\x93\x0c\xfb\x19V\rs,\x19\r\xeb>\xdc\x0ecQ\x9f\x0e\xdbd'
                 b'b\x0fSw%\x0f\xcb\x89\xe8\x10C\x9c\xab\t\xb2\x90\x01\n*\xa4'
                 b'\xc0f\xbby\xf6\x8d1\xa0l\xb3\xa7\xc6\xe2\xda\x1d\xedX\x10'
                 b'\xbb\xafn\x113\xfe\x80')
        self.assertTrue(code == truth)

    def test_decode_invalid_TEXT(self):
        """Try to decode invalid code."""

        code = 9 * b'\x00'
        with self.assertRaises(ValueError):
            code.decode('datamatrix.text')

    def test_search_nonTEXT(self):
        """Test that search_codec callback returns None for non-TEXT."""

        from ppf.datamatrix import codec_text
        self.assertTrue(codec_text.search_codec_text('invalid') is None)


if __name__ == '__main__':
    # This enables running the unit tests by running this script which is
    # much more convenient than 'python setup.py test' while developing tests.
    # Note: package-under-test needs to be in python-path
    unittest.main()
