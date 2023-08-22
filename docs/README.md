<img alt="ppf.datamatrix logo" src="./imgs/logo.svg" width="500em">

<img alt="pypi downloads/month" src="https://img.shields.io/pypi/dm/ppf.datamatrix.svg">

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

If you are working in a graphically enabled IPython terminal, you'll see your
datamatrix immediately:

![IPython integration](imgs/ipython.png)

Using the DataMatrix object, you get the SVG source like this:

```
myDataMatrix.svg()

'<?xml version="1.0" encoding="utf-8" ?><svg ...'
```

<img alt="Test! DataMatrix" src="./imgs/Test.svg" width="50em">

Use this on your website, to stamp a pdf, to uniquely identify a drawing, or
whatever you like.  Background and foreground color are configurable by
specifying fg and/or bg arguments.  Create a light blue matrix on a petrol
background like this:

```
myDataMatrix.svg(fg='#EEF', bg='#09D')
```

<img alt="Test! DataMatrix in red on blue background" src="./imgs/Test_colored.svg" width="50em">

Note: This sets the colors of the SVG.
It does *not* change the color of the representation inside your IPython terminal.


## Advanced Features

ppf.datamatrix supports a [variety of
encodings](https://en.m.wikipedia.org/wiki/Data_Matrix#Encoding), namely
EDIFACT ('datamatrix.edifact'), ASCII ('datamatrix.ascii'), X12
('datamatrix.X12'), C40 ('datamatrix.C40'), TEXT ('datamatrix.text').  These
are used to store your message inside the datamatrix code efficiently.
DataMatrix handles the encoding internally: If you just want to create a
DataMatrix, you don't have to care about any of this.  If you want to do
advanced stuff (designing your own form of matrix code, maybe), ppf.datamatrix
enables you to use its encoders.  After importing ppf.datamatrix, they are
available via the python codecs system:

```
import ppf.datamatrix

encoded = 'TEST'.encode('datamatrix.edifact')
encoded
b'\xf0PT\xd4'

decoded = encoded.decode('datamatrix.edifact')
decoded
'TEST'
```


# Installation

ppf.datamatrix is available via [pypi](https://pypi.org):

```
pip install ppf.datamatrix
```


# Still reading?

If you read this far, you're probably not here for the first time. If you use
and like this project, would you consider giving it a Github Star? (The button
is at the top of this website.) If not, maybe you're interested in one of
[my other projects](https://github.com/adrianschlatter/ppf.sample/blob/develop/docs/list_of_projects.md)?


# Contributing

Did you find a bug and would like to report it? Or maybe you've fixed it
already or want to help fixing it? That's great! Please read
[CONTRIBUTING](./CONTRIBUTING.md) to learn how to proceed from there.

To help ascertain that contributing to this project is a pleasant experience, we
have established a [code of conduct](./CODE_OF_CONDUCT.md). You can expect
everyone to adhere to it, just make sure you do as well.


# Change Log

* 0.1.2:    Fixed bug in RS correction data for each block
* 0.1.1:    Fixed bug in datamatrix.ascii encoding of digit pairs
* 0.1:      Initial port of datamatrix–svg
