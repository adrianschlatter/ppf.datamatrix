"""
ppf.datamatrix
++++++++++++++

ppf.datamatrix is a pure-python package to generate datamatrix codes.
"""
# flake8: noqa

# register codecs
from .codec_ascii import *
from .codec_edifact import *

# import every function, class, etc. that should be visible in the package
from .datamatrix import *

del datamatrix
del utils
