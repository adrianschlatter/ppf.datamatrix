# -*- coding: utf-8 -*-
"""
Unittests

Verify that DataMatrix encode works as expected:
- select the shortest encoding
- add the prefix \xe8 for the GS1 datamatrix

.. author: G.Baroncelli
"""

import unittest
import ppf.datamatrix as put


class Test_DataMatrix_Encode(unittest.TestCase):
    """Test DataMatrix._encode"""

    def test_shortest_encoding_text(self):
        """Verify that _encode select the shortest encoding"""
        msg = 'abcdefasfasdfas'
        enc = put.DataMatrix(msg)._encode_msg()
        self.assertEqual(enc, msg.encode('datamatrix.text'))

    def test_shortest_encoding_edifact(self):
        """Verify that _encode select the shortest encoding"""
        msg = "ABCDEFSFDGSFD........,,,,,,,,"
        enc = put.DataMatrix(msg)._encode_msg()
        self.assertEqual(enc, msg.encode('datamatrix.edifact'))

    def test_shortest_encoding_C40(self):
        """Verify that _encode select the shortest encoding"""
        msg = "ABCDEFDSFDGSDGFSDG."
        enc = put.DataMatrix(msg)._encode_msg()
        self.assertEqual(enc, msg.encode('datamatrix.C40'))

    def test_shortest_encoding_ascii(self):
        """Verify that _encode select the shortest encoding"""
        msg = "abcdefdfasfsfadsABCDEFSDFDSGDSG"
        enc = put.DataMatrix(msg)._encode_msg()
        self.assertEqual(enc, msg.encode('datamatrix.ascii'))

    def test_shortest_encoding_X12(self):
        """Verify that _encode select the shortest encoding"""
        msg = "ABCDEFDSFDGSDGFSDG>>"
        enc = put.DataMatrix(msg)._encode_msg()
        self.assertEqual(enc, msg.encode('datamatrix.X12'))

    def test_shortest_encoding_text_GS1(self):
        """Verify that _encode select the shortest encoding"""
        msg = 'abcdefasfasdfas'
        enc = put.DataMatrix(msg, gs1_datamatrix=True)._encode_msg()
        self.assertEqual(enc, b'\xe8' + msg.encode('datamatrix.text'))


if __name__ == '__main__':
    # This enables running the unit tests by running this script which is
    # much more convenient than 'python setup.py test' while developing tests.
    # Note: package-under-test needs to be in python-path
    unittest.main()
