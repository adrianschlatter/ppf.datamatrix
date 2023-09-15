# -*- coding: utf-8 -*-
"""
Unittests

Things shared between unittests are defined here to keep code DRY.

.. author: Adrian Schlatter
"""

import ppf.datamatrix as put
import sys

# Datamatrix has the following encodings:
# TEXT, C40, X12, EDIFACT, BASE256
# TEXT and C40 both encode the entire ASCII character table (in a
# different way).
# X12 and EDIFACT are subsets of ASCII characters.
# BASE256 is the (binary) 8-bit alphabet.

ASCII = bytes(range(128)).decode('ascii')
EDIFACT = bytes(range(32, 95)).decode('ascii')
X12 = '\r*> 01234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ'
BASE256 = bytes(range(256))


def msgs_from_alphabet(alphabet):
    """
    Creates test messages from alphabet

    Number of messages yielded is equal to length of alphabet. Length of
    messages varies from 0 to length of alphabet.
    """
    for i in range(len(alphabet)):
        if 2 * i > len(alphabet):
            msg = (alphabet[i:] +
                   alphabet[:2 * i - len(alphabet)])
        else:
            msg = alphabet[i:2 * i]

        yield msg


class Codec_Test(object):
    """
    Template class to test codec

    Create an actual test class by inheriting from this class and from
    unittest.TestCase. Make sure to customize class variables.
    """

    CODEC = 'name codec here'
    ALPHABET = 'list valid characters here'
    ALPHABET_ENC = b'what datamatrix-svg encodes ALPHABET to'
    KNOWN_PAIR = {'msg': 'A', 'enc': b'\x63'}
    CODEC_MODULE_NAME = 'codec_name'

    def test_consistency(self):
        """Verify that coding + decoding return the original message."""
        for msg in msgs_from_alphabet(self.ALPHABET):
            code = msg.encode(self.CODEC)
            decoded = code.decode(self.CODEC)
            self.assertEqual(decoded, msg)

    def test_raises(self):
        """Verify that error is raised for invalid code."""
        code = bytes([0])
        with self.assertRaises(ValueError):
            code.decode(self.CODEC)

    def test_encode_to_square_datamatrix(self):
        """Verify that encoding to square datamatrix works."""
        for msg in msgs_from_alphabet(self.ALPHABET):
            # assert that this does not raise:
            datamatrix = put.DataMatrix(msg)
            self.assertTrue(len(datamatrix.matrix) > 0)

    def test_encode_to_rect_datamatrix(self):
        """Verify that encoding to rectangular datamatrix works."""
        for msg in msgs_from_alphabet(self.ALPHABET):
            # assert that this does not raise:
            datamatrix = put.DataMatrix(msg, rect=True)
            m = datamatrix.matrix
            self.assertTrue(len(m) > 0)

    def test_encode_known(self):
        """Test single-char edifact encoding"""
        enc = self.KNOWN_PAIR['msg'].encode(self.CODEC)
        self.assertEqual(enc, self.KNOWN_PAIR['enc'])

    def test_encode_alphabet(self):
        """Encode entire alphabet and compare to datamatrix-svg."""
        enc = self.ALPHABET.encode(self.CODEC)
        self.assertEqual(enc, self.ALPHABET_ENC)

    def test_decode_invalid(self):
        """Try to decode invalid code."""

        code = 9 * b'\x00'
        with self.assertRaises(ValueError):
            code.decode(self.CODEC)

    def test_search_wrong_codec(self):
        """
        Test that search_codec callback returns None for non-matching
        codec.
        """

        full_mod_name = 'ppf.datamatrix.' + self.CODEC_MODULE_NAME
        __import__(full_mod_name)
        codec_mod = sys.modules[full_mod_name]
        self.assertTrue(codec_mod.search_codec('invalid') is None)
