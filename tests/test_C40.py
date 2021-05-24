# -*- coding: utf-8 -*-
"""
Unittests

Verify that datamatrix.C40 codec works as expected

.. author: Adrian Schlatter
"""

import unittest
# Following import needed to register C40 codec, even though 'put' not
# referenced in code:
import ppf.datamatrix as put  # noqa: F401

# C40 is able to encode any ASCII-character:
ASCII = bytes(range(128)).decode('ascii')


class Test_datamatrix_C40(unittest.TestCase):
    """Test codecs datamatrix.C40."""

    def test_consistency(self):
        """Verify that coding + decoding return the original message."""
        for i in range(128):
            if 2 * i > len(ASCII):
                msg = ASCII[i:] + ASCII[:3 * i - len(ASCII)]
            else:
                msg = ASCII[i:2 * i]

            code = msg.encode('datamatrix.C40')
            decoded = code.decode('datamatrix.C40')
            self.assertEqual(decoded, msg)

    def test_encode_known(self):
        """Encode and verify correctness."""
        code = 'A'.encode('datamatrix.C40')
        self.assertEqual(code, b'\xE6\xFEB')


if __name__ == '__main__':
    # This enables running the unit tests by running this script which is
    # much more convenient than 'python setup.py test' while developing tests.
    # Note: package-under-test needs to be in python-path
    unittest.main()
