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
__all__ = []

import codecs


def pack(ascii, tail=b''):
    """Packs groups of 4 ascii-encoded edifact chars into 3-byte words."""
    assert (len(ascii) + len(tail)) % 4 == 0

    raw = [code & 0x3F for code in ascii if 32 <= code <= 94]
    if len(raw) < len(ascii):
        raise ValueError('Invalid EDIFACT')
    raw += tail

    packed = []
    while len(raw) > 0:
        word = ((raw.pop(0) << 18) +
                (raw.pop(0) << 12) +
                (raw.pop(0) << 6) +
                (raw.pop(0)))
        packed += [word >> 16, (word >> 8) & 0xFF, (word >> 0) & 0xFF]

    return bytes(packed)


def encode_to_edifact(msg):
    """Encode message as datamatrix.edifact."""
    # edifact encoding works in groups of 4 characters:
    n_rest = len(msg) % 4

    if n_rest == 0:
        enc = b'\xF0' + pack(msg.encode('ascii'))
    elif n_rest == 1:
        if len(msg) < 2:
            enc = (b'\xF0' + pack(msg.encode('ascii'), b'\x1F\x00\x00'))
        else:
            enc = (b'\xF0' +
                   pack(msg[:-2].encode('ascii'), b'\x1F') +
                   msg[-2:].encode('datamatrix.ascii'))
    elif n_rest == 2:
        enc = b'\xF0' + pack(msg.encode('ascii'), b'\x1F\x00')
    else:
        enc = b'\xF0' + pack(msg.encode('ascii'), b'\x1F')

    return enc, len(enc)


def decode_from_edifact(enc):
    """Decode edifact-encoded message."""
    edifact = list(enc)
    if edifact[0] != 0xF0:
        raise ValueError(f'{enc} is not EDIFACT encoded')

    raw = []
    edifact.pop(0)
    ascii = b''
    while len(edifact) > 0:
        word = edifact.pop(0) << 16
        word += edifact.pop(0) << 8
        word += edifact.pop(0) << 0

        newraw = [(word >> 18) & 0x3F, (word >> 12) & 0x3F,
                  (word >> 6) & 0x3F, (word >> 0) & 0x3F]
        if 0x1F in newraw:
            raw += newraw[:newraw.index(0x1F)]
            ascii = bytes(edifact)
            break
        else:
            raw += newraw

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
