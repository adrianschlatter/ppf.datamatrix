# -*- coding: utf-8 -*-
"""
Unittests

Verify that datamatrix.X12 codec works as expected

.. author: Adrian Schlatter
"""

import unittest
from .common import X12
# Following import needed to register X12 codec, even though 'put' not
# referenced in code:
import ppf.datamatrix as put  # noqa: F401


class Test_datamatrix_X12(unittest.TestCase):
    """Test codecs datamatrix.X12."""

    def test_consistency(self):
        """Verify that coding + decoding return the original message."""
        for i in range(len(X12)):
            if 2 * i > len(X12):
                msg = X12[i:] + X12[:3 * i - len(X12)]
            else:
                msg = X12[i:2 * i]

            code = msg.encode('datamatrix.X12')
            decoded = code.decode('datamatrix.X12')
            self.assertEqual(decoded, msg)

    def test_encode_known(self):
        """Encode and verify correctness."""
        code = 'A'.encode('datamatrix.X12')
        self.assertEqual(code, b'\xEE\xFEB')


if __name__ == '__main__':
    # This enables running the unit tests by running this script which is
    # much more convenient than 'python setup.py test' while developing tests.
    # Note: package-under-test needs to be in python-path
    unittest.main()
