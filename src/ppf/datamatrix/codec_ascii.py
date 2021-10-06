#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
datamatrix.ascii codec
++++++++++++++++++++++

Adds datamatrix.ascii codec to python's codecs.

encoded = 'ABC'.encode('datamatrix.ascii')
decoded = encoded.decode('datamatrix.ascii')

datamatrix.ascii is encoded as follows:

- digits: are encoded pairwise as 130 + numeric_value(pair)
  (e.g., '60' is encoded as 130 + 60 = 190).
  If there is only a single digit, it is encoded as ASCII(char) + 1.
- non-digit ASCII chars are encoded as ASCII(char) + 1
- extended ASCII chars: are currently not supported by ppf.datamatrix

.. author: Adrian Schlatter
"""
__all__ = []

import codecs

DIGITS = '0123456789'


def encode_to_ascii(msg):
    """Encode to datamatrix.ascii."""
    enc = []
    i = 0
    while i < len(msg):
        if msg[i] in DIGITS and i + 1 < len(msg) and msg[i + 1] in DIGITS:
            enc.append(130 + int(msg[i:i + 2]))
            i += 1
        else:
            enc.append(list(msg[i].encode('ascii'))[0] + 1)
        i += 1

    return bytes(enc), len(enc)


def decode_from_ascii(code):
    """Decode datamatrix.ascii-encoded message."""
    msg = ''
    for c in code:
        if 130 <= c and c < 230:
            msg += f'{c-130:02d}'
        else:
            msg += bytes([c - 1]).decode('ascii')

    return msg, len(msg)


def search_codec_ascii(encoding_name):
    """Search function needed for registration in python codecs."""
    if encoding_name != 'datamatrix.ascii':
        return None

    return codecs.CodecInfo(encode_to_ascii,
                            decode_from_ascii,
                            name='datamatrix.ascii')


codecs.register(search_codec_ascii)
