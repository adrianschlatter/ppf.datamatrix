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


def encode_text_mode(msg, codepage, magic, multiset):
    """Encode to datamatrix text modes (C40, TEXT, X12)."""
    # Recipe:
    # 1. Declare codepage by magic code (e.g., b'\xE6' for C40)
    # 2. Convert chars in msg to raw-bytes by translation via codepage
    # 3. Pack 3 raw-bytes into 2 encoded bytes (words)
    # 4. Handle remaining chars in msg: Switch to ascii ('\xFE'), encode
    #    remaining chars to datamatrix.ascii
    # Special case: If msg is so short that we can't pack a single word,
    #               remain in datamatrix.ascii mode

    try:
        raw = sum([codepage[char] for char in msg], [])
    except KeyError:
        raise ValueError('Incompatible character in msg')

    # We want to encode the characters in msg:
    l_packable = (len(raw) // 3) * 3

    enc = b''
    if l_packable > 0:              # at least one word
        enc += magic                # switch to text mode
        topack = raw[:l_packable]
        enc += pack_words(topack)
        enc += b'\xFE'              # RTA-word (low-byte not necessary)
    else:
        topack = []                 # remain in ASCII mode

    if multiset:
        toascii = msg[len(list(tokenize(topack))):]
    else:
        toascii = msg[len(topack):]

    enc += toascii.encode('datamatrix.ascii')

    return enc, len(enc)


def decode_text_mode(enc, codepage, magic, multiset):
    """Decode datamatrix text-mode-encoded message (C40, TEXT, X12)."""
    enc = bytes(enc)
    magic = list(magic)[0]
    if enc[0] != magic:
        msg = enc.decode('datamatrix.ascii')
        return msg, len(msg)

    enc = enc[1:]   # drop magic code

    # a high-byte of 0xFE means RTA:
    pos = enc[::2].find(b'\xFE')
    words = enc[:2 * pos]
    remainder = enc[2 * pos + 1:]

    raw = unpack_words(words)
    if multiset is True:
        msg = ''.join([codepage[code] for code in tokenize(raw)])
    else:
        msg = ''.join([codepage[bytes([code])] for code in raw])
    msg += bytes(remainder).decode('datamatrix.ascii')

    return msg, len(msg)


def pack_words(raw):
    """3 raw bytes to 2 encoded bytes stuffing for datamatrix text modes."""
    if len(raw) % 3 != 0:
        raise ValueError('Length of "raw" must be integer multiple of 3')

    raw = list(raw)     # create a copy
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
    while len(words) >= 2:
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
