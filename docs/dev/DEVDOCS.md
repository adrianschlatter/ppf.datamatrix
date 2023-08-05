# Development Docs

This is the top-level development document. It provides an overview and links
to more specific documents.


## Porting - not re-inventing

ppf.datamatrix is a python port of
[datamatrix-svg](https://github.com/datalog/datamatrix-svg) which is written in
Javascript. The translation to Python is done so as to keep its counterpart in
datamatrix-svg clearly recognizable: The goal is not to invent something new
but to bring to Python what is already there for Javascript. If datamatrix-svg
fixes a bug or adds a feature, we want to be able to bring it over to
ppf.datamatrix as easily as possible. This seems particularly important as I
quite honestly don't have sufficient background in Galois theory and
Reed-Solomon codes to really understand how it works.

As a consequence, the Python code can turn out rather (or even very)
un-pythonic!

Of course, we wrap the datamatrix code in a class and also add some
functionality that datamatrix-svg does not have, such as .__repr__() or
._repr_svg_() methods (for IPython representation), or unittests. We write this
code - that does not have a counterpart in datamatrix-svg - in normal, pythonic
style.


## Codecs

Creating a datamatrix code requires encoding a text sting into a byte string.
Python has a mechanism for that (codecs) which we use and support.
"[Codecs](./codecs.md)" summarizes the datamatrix codecs and explains how they
work.


## Release-Process

"[Release-Process](./release-process.md)" describes how we do a release.

