# -*- coding: utf-8 -*-
"""
Unittests

Verify that DataMatrix class works as expected. Note that most testing is
done in the codec-specific tests. This file is for the rest.

.. author: Adrian Schlatter
"""

import unittest
import ppf.datamatrix as put


class Test_DataMatrix(unittest.TestCase):
    """Test DataMatrix"""

    def test_invalid_codec(self):
        """Verify that exception is raised for invalid codec"""

        with self.assertRaises(TypeError):
            put.DataMatrix('message', codecs=['invalid_codec'])
