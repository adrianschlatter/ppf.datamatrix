# -*- coding: utf-8 -*-
"""
Unittests

Verify that datamatrix.edifact codec works as expected

.. author: Adrian Schlatter
"""

import unittest
from .common import EDIFACT
import ppf.datamatrix as put


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
            datamatrix = put.DataMatrix(msg, rect=True)

            m = datamatrix.matrix
            self.assertTrue(len(m) > 0)

    def test_encode_known(self):
        """Test single-char edifact encoding"""
        enc = 'A'.encode('datamatrix.edifact')
        self.assertEqual(enc, b'\x42')

    def test_31(self):
        """
        Encode  msg resulting in EDIFACT [240, 31, 31, 31].

        Note: 31 is 'Return to ASCII Mode'
        """
        msg = 'G1<'
        enc = 'G1<'.encode('datamatrix.edifact')
        self.assertEqual(msg, enc.decode('datamatrix.edifact'))

    def test_encode_EDIFACT(self):
        """Encode entire alphabet and compare to datamatrix-svg."""
        truth = [240, 130, 24, 163, 146, 89, 167, 162, 154, 171, 178, 219, 175,
                 195, 28, 179, 211, 93, 183, 227, 158, 187, 243, 223, 191, 0,
                 16, 131, 16, 81, 135, 32, 146, 139, 48, 211, 143, 65, 20, 147,
                 81, 85, 151, 97, 150, 155, 113, 215, 159]
        enc = EDIFACT.encode('datamatrix.edifact')
        self.assertEqual(enc, bytes(truth))

    def test_decode_invalid_EDIFACT(self):
        """Try to decode invalid code."""

        code = 9 * b'\x00'
        with self.assertRaises(ValueError):
            code.decode('datamatrix.edifact')

    def test_search_nonEDIFACT(self):
        """Test that search_codec callback returns None for non-EDIFACT."""

        from ppf.datamatrix import codec_edifact
        self.assertTrue(codec_edifact.search_codec_edifact('invalid') is None)


if __name__ == '__main__':
    # This enables running the unit tests by running this script which is
    # much more convenient than 'python setup.py test' while developing tests.
    # Note: package-under-test needs to be in python-path
    unittest.main()
