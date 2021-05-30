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
__all__ = []

import codecs
from .codec_common import add_inverse_lookup
from .codec_common import encode_text_mode, decode_text_mode

# Source: https://en.m.wikipedia.org/wiki/Data_Matrix
X12 = '\r*> 0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'

codepage = {char: [code] for char, code in zip(X12, range(40))}
add_inverse_lookup(codepage)


def encode_to_X12(msg):
    """Encode to datamatrix.X12."""
    try:
        enc, length = encode_text_mode(msg, codepage, b'\xEE', False)
    except ValueError:
        raise ValueError(f'{msg} is not encodeable in X12')

    return enc, length


def decode_from_X12(enc):
    """Decode datamatrix.X12-encoded message."""
    try:
        msg, length = decode_text_mode(enc, codepage, b'\xEE', False)
    except ValueError:
        raise ValueError(f'{enc} is not valid X12 code')

    return msg, length


def search_codec_X12(encoding_name):
    """Search function needed for registration in python codecs."""
    if encoding_name != 'datamatrix.x12':
        return None

    return codecs.CodecInfo(encode_to_X12,
                            decode_from_X12,
                            name='datamatrix.X12')


codecs.register(search_codec_X12)
