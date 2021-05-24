#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
datamatrix.X12 codec
++++++++++++++++++++++

Adds datamatrix.X12 codec to python's codecs.

encoded = 'ABC'.encode('datamatrix.X12')
decoded = encoded.decode('datamatrix.X12')

.. author: Adrian Schlatter
"""

import codecs
from .codec_common import add_inverse_lookup, pack_words, unpack_words

# Source: https://en.m.wikipedia.org/wiki/Data_Matrix
X12 = '\r*> 0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'

codepage = {char: [code] for char, code in zip(X12, range(40))}
add_inverse_lookup(codepage)


def encode_to_X12(msg):
    """Encode to datamatrix.X12."""
    # Recipe:
    # 1. Declare X12: b'\xEE'
    # 2. Convert chars in msg to raw-bytes by translation via codepage
    # 3. Pack 3 raw-bytes into 2 encoded bytes (words)
    # 4. Handle remaining chars in msg: Switch to ascii ('\xFE'), encode
    #    remaining chars to datamatrix.ascii

    try:
        raw = sum([codepage[char] for char in msg], [])
    except KeyError:
        raise ValueError(f'{msg} is not encodable in X12')

    n_words = len(raw) // 3
    topack = raw[:n_words * 3]
    toascii = msg[len(topack):]

    enc = b'\xEE' + pack_words(topack)
    if len(toascii) > 0:
        enc += b'\xFE'
        enc += toascii.encode('datamatrix.ascii')

    return enc, len(enc)


def decode_from_X12(enc):
    """Decode datamatrix.X12-encoded message."""
    enc = bytes(enc)
    if enc[0] != 0xEE:
        raise ValueError(f'{enc} is not valid X12 code')

    enc = enc[1:]
    # if there is an b'\xFE' at an even position, it means 'switch to ASCII'
    # note: in an odd position, it is just a coincidence to word packing.
    pos = enc[::2].find(b'\xFE')
    if pos > -1:
        words = enc[: 2 * pos]
        remainder = enc[2 * pos + 1:]
    else:
        words = enc
        remainder = b''

    raw = unpack_words(words)
    msg = ''.join([codepage[bytes([code])] for code in raw])
    msg += remainder.decode('datamatrix.ascii')

    return msg, len(msg)


def search_codec_X12(encoding_name):
    """Search function needed for registration in python codecs."""
    if encoding_name != 'datamatrix.x12':
        return None

    return codecs.CodecInfo(encode_to_X12,
                            decode_from_X12,
                            name='datamatrix.X12')


codecs.register(search_codec_X12)
