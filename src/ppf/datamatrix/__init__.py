"""
ppf.datamatrix
++++++++++++++

ppf.datamatrix is a pure-python package to generate datamatrix codes.
"""
# flake8: noqa

# register codecs
from .codec_ascii import *
from .codec_edifact import *
from .codec_C40 import *
from .codec_text import *
from .codec_X12 import *

# import every function, class, etc. that should be visible in the package
from .datamatrix import *

del datamatrix
del utils
