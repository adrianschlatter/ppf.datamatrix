# -*- coding: utf-8 -*-
"""
Unittests

Verify that datamatrix.text codec works as expected

.. author: Adrian Schlatter
"""

import unittest
from .common import ASCII
# Following import needed to register text codec, even though 'put' not
# referenced in code:
import ppf.datamatrix as put  # noqa: F401


class Test_datamatrix_text(unittest.TestCase):
    """Test codecs datamatrix.text."""

    def test_consistency(self):
        """Verify that coding + decoding return the original message."""
        for i in range(128):
            if 2 * i > len(ASCII):
                msg = ASCII[i:] + ASCII[:3 * i - len(ASCII)]
            else:
                msg = ASCII[i:2 * i]

            code = msg.encode('datamatrix.text')
            decoded = code.decode('datamatrix.text')
            self.assertEqual(decoded, msg)

    def test_encode_known(self):
        """Encode and verify correctness."""
        code = 'A'.encode('datamatrix.text')
        self.assertEqual(code, b'\xE9\xFEB')


if __name__ == '__main__':
    # This enables running the unit tests by running this script which is
    # much more convenient than 'python setup.py test' while developing tests.
    # Note: package-under-test needs to be in python-path
    unittest.main()
