AsciiDoc.py
===========

[![Build Status](https://github.com/asciidoc/asciidoc-py3/workflows/Test/badge.svg?branch=master)](https://github.com/asciidoc/asciidoc-py3/actions?query=workflow%3ATest+branch%3Amaster)
[![codecov](https://codecov.io/gh/asciidoc-py/asciidoc-py/branch/main/graph/badge.svg?token=fNh3QlLTw0)](https://codecov.io/gh/asciidoc-py/asciidoc-py)
[![PyPI version](https://badge.fury.io/py/asciidoc.svg)](https://badge.fury.io/py/asciidoc)

AsciiDoc is a text document format for writing notes, documentation,
articles, books, ebooks, slideshows, web pages, man pages and blogs.
AsciiDoc files can be translated to many formats including HTML, PDF,
EPUB, man page.

AsciiDoc.py is a legacy processor for this syntax, handling an older
rendition of AsciiDoc. As such, this will not properly handle the
[current AsciiDoc specification](https://projects.eclipse.org/projects/technology.asciidoc).
It is suggested that unless you specifically require the AsciiDoc.py
toolchain, you should find a processor that handles the modern AsciiDoc
syntax.

AsciiDoc.py is highly configurable: both the AsciiDoc source file syntax
and the backend output markups (which can be almost any type of
SGML/XML markup) can be customized and extended by the user.

## Prerequisites

AsciiDoc.py is written in Python so you need a Python interpreter
(version 3.5 or later) to execute asciidoc(1). You can install Python using the
package manager for your OS or by downloading it from the official Python
website http://www.python.org.

Additionally, you wil need:

* DocBook XSL Stylesheets 1.76.1
* xsltproc (libxml 20706, libxslt 10126 and libexslt 815).
* w3m 0.5.2
* dblatex 0.3
* FOP 0.95

to enable the full AsciiDoc.py toolchain.

## Obtaining AsciiDoc.py

Documentation and installation instructions are on the AsciiDoc.py website
https://asciidoc.org/. Simply, you should use use pip to install it:

```
pip3 install asciidoc
```

## Contributing

To contribute and test your changes, you will need to install:
* flake8
* pytest
* pytest-mock

To lint the codebase: `python3 -m flake8`

AsciiDoc.py has the following types of tests:
1. doctests: `python3 -m asciidoc.asciidoc --doctest`
1. unit tests: `python3 -m pytest`
1. integration tests: `python3 tests/testasciidoc.py`

## LICENSE

Copyright (C) 2002-2013 Stuart Rackham.
Copyright (C) 2013-2021 AsciiDoc.py Contributors.

Free use of this software is granted under the terms of the GNU General
Public License version 2 (GPLv2).
