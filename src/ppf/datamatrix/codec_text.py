#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
datamatrix.text codec
++++++++++++++++++++++

Adds datamatrix.text codec to python's codecs.

encoded = 'ABC'.encode('datamatrix.text')
decoded = encoded.decode('datamatrix.text')

.. author: Adrian Schlatter
"""
__all__ = []

import codecs
from .codec_common import set1, set2, add_inverse_lookup
from .codec_common import encode_text_mode, decode_text_mode

# Source: https://en.m.wikipedia.org/wiki/Data_Matrix
set0 = ' 0123456789abcdefghijklmnopqrstuvwxyz'
set3 = '`ABCDEFGHIJKLMNOPQRSTUVWXYZ{|}~' + b'\x7f'.decode('ascii')

codepage = {char: [code] for char, code in zip(set0, range(3, 40))}
codepage = {**codepage,
            **{char: [0, code] for char, code in zip(set1, range(40))}}
codepage = {**codepage,
            **{char: [1, code] for char, code in zip(set2, range(40))}}
codepage = {**codepage,
            **{char: [2, code] for char, code in zip(set3, range(40))}}

add_inverse_lookup(codepage)


def encode_to_text(msg):
    """Encode to datamatrix.text."""
    return encode_text_mode(msg, codepage, b'\xEF', True)


def decode_from_text(enc):
    """Decode datamatrix.text-encoded message."""
    try:
        msg, length = decode_text_mode(enc, codepage, b'\xEF', True)
    except ValueError:
        raise ValueError(f'{bytes(enc)} is not valid TEXT code')

    return msg, length


def search_codec_text(encoding_name):
    """Search function needed for registration in python codecs."""
    if encoding_name != 'datamatrix.text':
        return None

    return codecs.CodecInfo(encode_to_text,
                            decode_from_text,
                            name='datamatrix.text')


codecs.register(search_codec_text)
