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
    # 1. Declace codepage by magic code (e.g., b'\xE6' for C40)
    # 2. Convert chars in msg to raw-bytes by translation via codepage
    # 3. Pack 3 raw-bytes into 2 encoded bytes (words)
    # 4. Handle remaining chars in msg: Switch to ascii ('\xFE'), encode
    #    remaining chars to datamatrix.ascii
    #
    # Important special case:
    # C40 (e.g.) uses multiple sets (see above). Default is set0 but set0
    # has codes to switch to set1, set2, or set3 for the following code.
    # Example: 'a' => [2, 1], where 2 is the 'switch to set3' code and 1
    # is the code for 'a' in set3.
    # When packing raw-bytes into words, it can happen that the 'switch
    # to setX' and the code after it are packed into separate words.
    # In particular, it may happen that the 'switch to setX' code is packed
    # into the *last* word and the code after it is *not* packed into a word
    # (because there are <3 raw bytes remaining). In that case, we *do*
    # pack the 'switch to setX' into the last word. It will be immediately
    # followed by the 'switch to ascii' code, anyway. We have to make sure
    # that the character "split in half" is added to the "ascii tail".

    try:
        raw = sum([codepage[char] for char in msg], [])
    except KeyError:
        raise ValueError('Incompatible character in msg')

    n_words = len(raw) // 3
    topack = raw[:n_words * 3]
    if multiset:
        toascii = msg[len(list(tokenize(topack))):]
    else:
        toascii = msg[len(topack):]

    enc = magic + pack_words(topack)
    if len(toascii) > 0:
        enc += b'\xFE'
        enc += toascii.encode('datamatrix.ascii')

    return enc, len(enc)


def decode_text_mode(enc, codepage, magic, multiset):
    """Decode datamatrix text-mode-encoded message (C40, TEXT, X12)."""
    enc = bytes(enc)
    magic = list(magic)[0]
    if enc[0] != magic:
        raise ValueError()

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
    if multiset:
        msg = ''.join([codepage[code] for code in tokenize(raw)])
    else:
        msg = ''.join([codepage[bytes([code])] for code in raw])
    msg += remainder.decode('datamatrix.ascii')

    return msg, len(msg)


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
