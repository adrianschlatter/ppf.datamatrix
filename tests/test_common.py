# -*- coding: utf-8 -*-
"""
Unittests

Verify that datamatrix.C40 codec works as expected

.. author: Adrian Schlatter
"""

import unittest
from .common import ASCII
import ppf.datamatrix as put


class Test_Common(unittest.TestCase):
    """Test codec_common"""

    def test_pack_words_of_invalid_raw(self):
        """Try to pack invalid raw."""

        raw = 4 * b'\x00'  # length not multiple of 4
        from ppf.datamatrix import codec_common
        with self.assertRaises(ValueError):
            codec_common.pack_words(raw)

    def test_unpack_invalid_words(self):
        """Try to unpack invalid words."""

        words = 3 * b'\x00'  # length not even
        from ppf.datamatrix import codec_common
        with self.assertRaises(ValueError):
            codec_common.unpack_words(words)
