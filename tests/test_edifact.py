# -*- coding: utf-8 -*-
"""
Unittests

Verify that datamatrix.edifact codec works as expected

.. author: Adrian Schlatter
"""

import ppf.datamatrix
import unittest
from .common import EDIFACT, Codec_Test


class Test_datamatrix_edifact(Codec_Test, unittest.TestCase):
    """Test codecs datamatrix.edifact."""

    CODEC = 'datamatrix.edifact'
    ALPHABET = EDIFACT
    ALPHABET_ENC = (
        b'\xf0\x82\x18\xa3\x92Y\xa7\xa2\x9a\xab\xb2\xdb\xaf\xc3'
        b'\x1c\xb3\xd3]\xb7\xe3\x9e\xbb\xf3\xdf\xbf\x00\x10\x83\x10Q\x87'
        b' \x92\x8b0\xd3\x8fA\x14\x93QU\x97a\x96\x9bq\xd7\x9f')
    KNOWN_PAIR = {'msg': 'A', 'enc': b'\x42'}
    CODEC_MODULE_NAME = 'codec_edifact'

    def test_31(self):
        """
        Encode  msg resulting in EDIFACT [240, 31, 31, 31].

        Note: 31 is 'Return to ASCII Mode'
        """
        msg = 'G1<'
        enc = 'G1<'.encode('datamatrix.edifact')
        self.assertEqual(msg, enc.decode('datamatrix.edifact'))


if __name__ == '__main__':
    # This enables running the unit tests by running this script which is
    # much more convenient than 'python setup.py test' while developing tests.
    # Note: package-under-test needs to be in python-path
    unittest.main()
