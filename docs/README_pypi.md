# ppf.datamatrix

ppf.datamatrix is a pure-python package to generate datamatrix codes in SVG.
Also, it integrates nicely in IPython.

ppf.datamatrix has been ported from [datalog's
datamatrix-svg](https://github.com/datalog/datamatrix-svg), which is written in
javascript.  If you like to see what you'll get before installation, check out
their [nice web demo](https://datalog.github.io/demo/datamatrix-svg).

Creating a datamatrix with ppf.datamatrix is as easy as

```
from ppf.datamatrix import DataMatrix

myDataMatrix = DataMatrix('Test!')
```

A graphically enabled IPython terminal will even represent myDataMatrix as a
picture.

Check out the project website to find out  more!
