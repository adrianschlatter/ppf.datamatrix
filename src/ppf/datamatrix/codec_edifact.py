#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
datamatrix.edifact codec
++++++++++++++++++++++++

Adds datamatrix.edifact codec to python's codecs.

encoded = 'ABC'.encode('datamatrix.edifact')
decoded = encoded.decode('datamatrix.edifact')

.. author: Adrian Schlatter
"""

import codecs


def encode_to_edifact(msg):
    """Encode message as datamatrix.edifact."""
    # edifact encoding works in groups of 4 characters
    n_groups = len(msg) // 4

    enc = [240]
    if n_groups > 0:
        raw = [code & 0x3F
               for code in msg[:4 * n_groups].encode('ascii')
               if 32 <= code <= 94]
        if len(raw) < 4 * n_groups:
            raise ValueError(f'{msg} is not valid EDIFACT')

        while len(raw) > 0:
            word = ((raw.pop(0) << 18) +
                    (raw.pop(0) << 12) +
                    (raw.pop(0) << 6) +
                    (raw.pop(0)))
            enc += [word >> 16, (word >> 8) & 0xFF, (word >> 0) & 0xFF]

    if len(msg) % 4 == 0:
        return bytes(enc), len(enc)
    else:
        enc = bytes(enc + [31]) + msg[4 * n_groups:].encode('datamatrix.ascii')
        return enc, len(enc)


def decode_from_edifact(code):
    """Decode edifact-encoded message."""
    # make sure code is bytes (and not memoryview):
    code = bytes(code)
    if code[0] != 240:
        raise ValueError(f'{code} is not EDIFACT encoded')
    else:
        code = code[1:]
        if b'\x1F' in code:
            edifact, ascii = code.split(b'\x1F')
        else:
            edifact = code
            ascii = b''

        raw = []
        edifact = list(edifact)
        while len(edifact) > 0:
            word = edifact.pop(0) << 16
            word += edifact.pop(0) << 8
            word += edifact.pop(0) << 0

            raw += [(word >> 18) & 0x3F, (word >> 12) & 0x3F,
                    (word >> 6) & 0x3F, (word >> 0) & 0x3F]

        msg = bytes([code if code >= 0x20 else code | 0x40
                    for code in raw]).decode('ascii')

    msg += ascii.decode('datamatrix.ascii')

    return msg, len(msg)


def search_codec_edifact(encoding_name):
    """Search function needed for registration in python codecs."""
    if encoding_name != 'datamatrix.edifact':
        return None

    return codecs.CodecInfo(encode_to_edifact, decode_from_edifact,
                            name='datamatrix.edifact')


codecs.register(search_codec_edifact)
