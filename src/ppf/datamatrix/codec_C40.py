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

import codecs
from .codec_common import set1, set2, add_inverse_lookup, tokenize
from .codec_common import pack_words, unpack_words

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
    # Recipe:
    # 1. Declace C40: b'\xE6'
    # 2. Convert chars in msg to raw-bytes by translation via codepage
    # 3. Pack 3 raw-bytes into 2 encoded bytes (words)
    # 4. Handle remaining chars in msg: Switch to ascii ('\xFE'), encode
    #    remaining chars to datamatrix.ascii
    #
    # Important special case:
    # C40 uses multiple sets (see above). Default is set0 but set0 has
    # codes to switch to set1, set2, or set3 for the following code.
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

    raw = sum([codepage[char] for char in msg], [])

    n_words = len(raw) // 3
    topack = raw[:n_words * 3]
    toascii = msg[len(list(tokenize(topack))):]

    enc = b'\xE6' + pack_words(topack)
    if len(toascii) > 0:
        enc += b'\xFE'
        enc += toascii.encode('datamatrix.ascii')

    return enc, len(enc)


def decode_from_C40(enc):
    """Decode datamatrix.C40-encoded message."""
    enc = bytes(enc)
    if enc[0] != 0xE6:
        raise ValueError('f{enc} is not valid C40 code')

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
    msg = ''.join([codepage[code] for code in tokenize(raw)])
    msg += remainder.decode('datamatrix.ascii')

    return msg, len(msg)


def search_codec_C40(encoding_name):
    """Search function needed for registration in python codecs."""
    if encoding_name != 'datamatrix.c40':
        return None

    return codecs.CodecInfo(encode_to_C40,
                            decode_from_C40,
                            name='datamatrix.C40')


codecs.register(search_codec_C40)
