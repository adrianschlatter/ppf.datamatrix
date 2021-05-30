"""
ppf.datamatrix
++++++++++++++


ppf.datamatrix is a pure-python package to generate datamatrix codes.

Example:

    from ppf.datamatrix import DataMatrix
    my_matrix = DataMatrix('Write your message here')
    # get svg of datamatrix:
    svg = my_matrix.svg()
"""

# register codecs
from .codec_ascii import *
from .codec_edifact import *
from .codec_C40 import *
from .codec_text import *
from .codec_X12 import *

# import every function, class, etc. that should be visible in the package
from .datamatrix import *

del datamatrix
del codec_ascii
del codec_edifact
del codec_C40
del codec_text
del codec_X12
del codec_common
del utils
