#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ported from:
https://raw.githubusercontent.com/datalog/datamatrix-svg/master/datamatrix.js

.. author: Adrian Schlatter
"""

# flake8: noqa: E741

from .utils import export

svg_template = \
    '<?xml version="1.0" encoding="utf-8" ?>' \
    '<svg baseProfile="tiny" version="1.2" ' \
    'height="{size}px" width="{size}px" ' \
    'style="background-color:{bg}" ' \
    'xmlns="http://www.w3.org/2000/svg" ' \
    'xmlns:ev="http://www.w3.org/2001/xml-events" ' \
    'xmlns:xlink="http://www.w3.org/1999/xlink"><defs/>' \
    '<path d="M1,1.5 {path_cmds}" stroke="{fg}" stroke-width="1"/></svg>'


@export
class DataMatrix():
    """
    Creates a datamatrix code for message 'msg'.

    Currently supports EDIFACT messages and nothing more.
    """

    def __init__(self, msg):
        self._msg = msg

    def __repr__(self):
        return f"DataMatrix('{self._msg}')"

    def _repr_svg_(self):
        return self.svg(bg='#000', fg='#FFF')

    def _svg_path_iterator(self):
        size = len(self.matrix)

        for line in self.matrix:
            i = 0
            while(i < size):
                color = line[i]
                i0 = i
                while(i < size and line[i] == color):
                    i = i + 1

                length = i - i0
                if color == 1:
                    yield 'h'
                    yield str(length)
                else:
                    yield 'm'
                    yield f'{length},0'
            yield 'm'
            yield f'{-size},1'

    def svg(self, fg='#000', bg='#FFF'):
        cmds = ''.join(self._svg_path_iterator())
        return svg_template.format(fg=fg, bg=bg, path_cmds=cmds,
                                   size=len(self.matrix) + 2)

    @property
    def message(self):
        return self._msg

    @property
    def matrix(self):
        rct = False

        def bit(x, y):
            M[y] = M.get(y, {})
            M[y][x] = 1

        # unescape( encodeURI( text ) );
        M = {}
        enc = []
        for codec in ['datamatrix.ascii', 'datamatrix.edifact']:
            try:
                enc.append(self._msg.encode(codec))
            except ValueError:
                pass
        enc = min(enc, key=len)
        enc = {i: c for i, c in enumerate(enc)}
        el = len(enc)

        nc = 1
        nr = 1  # symbol size, regions, region size
        j = - 1
        b = 1   # compute symbol size

        rs = [0] * 70   # reed solomon code
        rc = [0] * 70
        lg = [0] * 256  # log / exp table for multiplication
        ex = [0] * 255

        if not rct:  # square code
            w = h = 6
            i = 2     # size increment
            # rs checkwords
            k = [5, 7, 10, 12, 14, 18, 20, 24, 28, 36, 42, 48, 56, 68,
                 84, 112, 144, 192, 224, 272, 336, 408, 496, 620]

        l = 0
        while True:
            j += 1
            if j == len(k):
                raise ValueError('Message is too long')

            if(w > 11 * i):
                i = 4 + i & 12  # advance increment

            h += i
            w = h
            l = (w * h) >> 3

            if l - k[j] >= el:
                break

        if(w > 27):
            nr = nc = 2 * (w // 54 | 0) + 2  # regions
        if(l > 255):
            b = 2 * (l >> 9) + 2            # blocks

        s = k[j]        # rs checkwords
        fw = w // nc     # region size
        fh = h // nr

        # first padding
        if(el < l - s):
            enc[el] = 129
            el += 1

        # more padding
        while(el < l - s):
            enc[el] = (((149 * (el + 1)) % 253) + 130) % 254
            el += 1

        # Reed Solomon error detection and correction
        s //= b

        # log / exp table of Galois field
        j = 1
        for i in range(255):
            ex[i] = j
            lg[j] = i
            j += j

            if(j > 255):
                j ^= 301    # 301 == a^8 + a^5 + a^3 + a^2 + 1

        # RS generator polynomial
        rs[s] = 0
        for i in range(1, s + 1):
            rs[s - i] = 1
            for j in range(s - i, s):
                rs[j] = rs[j + 1] ^ ex[(lg[rs[j]] + i) % 255]

        # RS correction data for each block
        for c in range(b):
            for i in range(s + 1):
                rc[i] = 0
            for i in range(c, el, b):
                x = rc[0] ^ enc[i]
                for j in range(s):
                    if x:
                        rc[j] = rc[j + 1] ^ ex[(lg[rs[j]] + lg[x]) % 255]
                    else:
                        rc[j] = 0

            # interleaved correction data
            for i in range(s):
                enc[el + c + i * b] = rc[i]

        # layout perimeter finder pattern
        # horizontal
        for i in range(0, h + 2 * nr, fh + 2):
            for j in range(0, w + 2 * nc):
                bit(j, i + fh + 1)
                if((j & 1) == 0):
                    bit(j, i)

        # vertical
        for i in range(0, w + 2 * nc, fw + 2):
            for j in range(h):
                bit(i, j + (j // fh | 0) * 2 + 1)
                if((j & 1) == 1):
                    bit(i + fw + 1, j + (j // fh | 0) * 2)

        s = 2   # step
        c = 0   # column
        r = 4   # row
        b = [   # nominal byte layout
            0,  0,
            -1,  0,
            -2,  0,
            0, -1,
            -1, -1,
            -2, -1,
            -1, -2,
            -2, -2]

        # diagonal steps
        i = 0
        while True:
            if i >= l:
                break

            if (r == h - 3 and c == - 1):
                k = [          # corner A layout
                    w, 6 - h,
                    w, 5 - h,
                    w, 4 - h,
                    w, 3 - h,
                    w - 1, 3 - h,
                    3,     2,
                    2,     2,
                    1,     2]
            elif r == h + 1 and c == 1 and (w & 7) == 0 and (h & 7) == 6:
                k = [          # corner D layout
                    w - 2,     -h,
                    w - 3,     -h,
                    w - 4,     -h,
                    w - 2, -1 - h,
                    w - 3, -1 - h,
                    w - 4, -1 - h,
                    w - 2, -2,
                    -1,     -2]
            else:
                if r == 0 and c == w - 2 and (w & 3):
                    r -= s
                    c += s
                    continue   # corner B: omit upper left
                if r < 0 or c >= w or r >= h or c < 0:  # outside
                    s = -s     # turn around
                    r += 2 + s // 2
                    c += 2 - s // 2

                    while r < 0 or c >= w or r >= h or c < 0:
                        r -= s
                        c += s

                if r == h - 2 and c == 0 and (w & 3):
                    k = [       # corner B layout
                        w - 1, 3 - h,
                        w - 1, 2 - h,
                        w - 2, 2 - h,
                        w - 3, 2 - h,
                        w - 4, 2 - h,
                        0,     1,
                        0,     0,
                        0,    -1]
                elif r == h - 2 and c == 0 and (w & 7) == 4:
                    k = [       # corner C layout
                        w - 1, 5 - h,
                        w - 1, 4 - h,
                        w - 1, 3 - h,
                        w - 1, 2 - h,
                        w - 2, 2 - h,
                        0,     1,
                        0,     0,
                        0,    -1]
                elif r == 1 and c == w - 1 and (w & 7) == 0 and (h & 7) == 6:
                    r -= s
                    c += s
                    continue    # omit corner D
                else:
                    k = b       # nominal L - shape layout

            # layout each bit
            el = enc[i]
            i += 1
            j = 0
            while True:
                if el <= 0:
                    break

                if el & 1:
                    x = c + k[j]
                    y = r + k[j + 1]

                    # wrap around
                    if x < 0:
                        x += w
                        y += 4 - ((w + 4) & 7)
                    if y < 0:
                        y += h
                        x += 4 - ((h + 4) & 7)

                    # region gap
                    bit(x + 2 * (x // fw | 0) + 1, y + 2 * (y // fh | 0) + 1)

                j += 2
                el >>= 1

            r -= s
            c += s

        # unfilled corner
        i = w
        while True:
            if not i & 3:
                break

            bit(i, i)
            i -= 1

        matrix = []
        size = len(M)
        for j in range(size):
            matrix.append([])
            for i in range(size):
                x = M[j].get(i, 0)
                matrix[j].append(M[j].get(i, 0))

        return matrix
