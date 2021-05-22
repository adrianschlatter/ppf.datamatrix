# -*- coding: utf-8 -*-
"""
Unittests

Verify that datamatrix.edifact codec works as expected

.. author: Adrian Schlatter
"""

import unittest
import ppf.datamatrix as put

EDIFACT = bytes(range(32, 95)).decode('ascii')


class Test_datamatrix_edifact(unittest.TestCase):
    """Test codecs datamatrix.edifact."""

    def test_consistency(self):
        """Verify that coding + decoding return the original message."""
        for i in range(len(EDIFACT)):
            if 2 * i > len(EDIFACT):
                msg = EDIFACT[i:] + EDIFACT[:3 * i - len(EDIFACT)]
            else:
                msg = EDIFACT[i:2 * i]
            print(f'{i}: "{msg}"')

            code = msg.encode('datamatrix.edifact')
            decoded = code.decode('datamatrix.edifact')
            self.assertEqual(decoded, msg)

    def test_encode_known(self):
        """Encode and verify correctness."""
        code = 'A'.encode('datamatrix.edifact')
        self.assertEqual(code, b'\xf0\x1fB')


if __name__ == '__main__':
    # This enables running the unit tests by running this script which is
    # much more convenient than 'python setup.py test' while developing tests.
    # Note: package-under-test needs to be in python-path
    unittest.main()
