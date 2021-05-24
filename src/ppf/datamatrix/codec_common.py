#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Code shared among several codecs
++++++++++++++++++++++++++++++++

.. author: Adrian Schlatter
"""

# Source: https://en.m.wikipedia.org/wiki/Data_Matrix
set1 = bytes(range(32)).decode('ascii')
set2 = '!"#$%&\'()*+,-./:;<=>?@[\\]^_'


def add_inverse_lookup(codepage):
    """Add value: key pairs to existing key: value pairs in codepage."""
    all_chars = list(codepage.keys())
    for char in all_chars:
        code = codepage[char]
        codepage[bytes(code)] = char


def pack_words(raw):
    """3 raw bytes to 2 encoded bytes stuffing for datamatrix text modes."""
    if len(raw) % 3 != 0:
        raise ValueError('Length of "raw" must be integer multiple of 3')

    enc = []
    while len(raw) > 0:
        word = ((raw.pop(0) * 40**2) +
                (raw.pop(0) * 40**1) +
                (raw.pop(0) * 40**0) +
                1)
        enc += [word >> 8, word & 0xFF]

    return bytes(enc)


def unpack_words(words):
    """2 encoded bytes to 3 raw bytes unstuffing for datamatrix text modes."""
    if len(words) % 2 != 0:
        raise ValueError('Length of "words" must be even')

    words = list(words)
    raw = []
    while len(words) > 0:
        word = ((words.pop(0) << 8) +
                (words.pop(0) << 0))
        word -= 1
        raw += [word // 40**2,
                (word % 40**2) // 40**1,
                ((word % 40**2) % 40**1) // 40**0]

    return bytes(raw)


def tokenize(enc):
    """Yield tokens from encoding 'enc'.

    Yields next byte if it is not a 'switch alphabet' code. If it is,
    yields a code pair (switch alphabet code + code following it.
    """
    buffer = b''
    for code in iter(enc):
        if buffer:
            yield buffer + bytes([code])
            buffer = b''
        elif code >= 3:
            yield bytes([code])
        else:
            buffer = bytes([code])
