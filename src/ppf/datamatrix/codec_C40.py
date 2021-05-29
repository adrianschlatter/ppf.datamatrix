#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
datamatrix.C40 codec
++++++++++++++++++++++

Adds datamatrix.C40 codec to python's codecs.

encoded = 'ABC'.encode('datamatrix.C40')
decoded = encoded.decode('datamatrix.C40')

.. author: Adrian Schlatter
"""
__all__ = []

import codecs
from .codec_common import set1, set2, add_inverse_lookup
from .codec_common import encode_text_mode, decode_text_mode

# Source: https://en.m.wikipedia.org/wiki/Data_Matrix
set0 = ' 0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
set3 = '`abcdefghijklmnopqrstuvwxyz{|}~' + b'\x7f'.decode('ascii')

codepage = {char: [code] for char, code in zip(set0, range(3, 40))}
codepage = {**codepage,
            **{char: [0, code] for char, code in zip(set1, range(40))}}
codepage = {**codepage,
            **{char: [1, code] for char, code in zip(set2, range(40))}}
codepage = {**codepage,
            **{char: [2, code] for char, code in zip(set3, range(40))}}

add_inverse_lookup(codepage)


def encode_to_C40(msg):
    """Encode to datamatrix.C40."""
    return encode_text_mode(msg, codepage, b'\xE6', True)


def decode_from_C40(enc):
    """Decode datamatrix.C40-encoded message."""
    try:
        msg, length = decode_text_mode(enc, codepage, b'\xE6', True)
    except ValueError:
        raise ValueError(f'{enc} is not valid C40 code')

    return msg, length


def search_codec_C40(encoding_name):
    """Search function needed for registration in python codecs."""
    if encoding_name != 'datamatrix.c40':
        return None

    return codecs.CodecInfo(encode_to_C40,
                            decode_from_C40,
                            name='datamatrix.C40')


codecs.register(search_codec_C40)
