#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
datamatrix.ascii codec
++++++++++++++++++++++

Adds datamatrix.ascii codec to python's codecs.

encoded = 'ABC'.encode('datamatrix.ascii')
decoded = encoded.decode('datamatrix.ascii')

.. author: Adrian Schlatter
"""
__all__ = []

import codecs


def encode_to_ascii(msg):
    """Encode to datamatrix.ascii."""
    enc = msg.encode('ascii')
    return bytes([code + 1 for code in enc]), len(msg)


def decode_from_ascii(code):
    """Decode datamatrix.ascii-encoded message."""
    return bytes([c - 1 for c in code]).decode('ascii'), len(code)


def search_codec_ascii(encoding_name):
    """Search function needed for registration in python codecs."""
    if encoding_name != 'datamatrix.ascii':
        return None

    return codecs.CodecInfo(encode_to_ascii,
                            decode_from_ascii,
                            name='datamatrix.ascii')


codecs.register(search_codec_ascii)
