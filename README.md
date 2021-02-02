AsciiDoc
========

[![Build Status](https://github.com/asciidoc/asciidoc-py3/workflows/Test/badge.svg?branch=master)](https://github.com/asciidoc/asciidoc-py3/actions?query=workflow%3ATest+branch%3Amaster)

__This branch is tracking the alpha, in-progress 10.x release. For the stable 9.x code,
please go to the [9.x branch](https://github.com/asciidoc/asciidoc-py3/tree/9.x)!__

AsciiDoc is a text document format for writing notes, documentation,
articles, books, ebooks, slideshows, web pages, man pages and blogs.
AsciiDoc files can be translated to many formats including HTML, PDF,
EPUB, man page.

AsciiDoc is highly configurable: both the AsciiDoc source file syntax
and the backend output markups (which can be almost any type of
SGML/XML markup) can be customized and extended by the user.

## Prerequisites

AsciiDoc is written in Python so you need a Python interpreter
(version 3.5 or later) to execute asciidoc(1). You can install Python using the
package manager for your OS or by downloading it from the official Python
website http://www.python.org.

## Obtaining AsciiDoc

Documentation and installation instructions are on the AsciiDoc website
http://asciidoc.org/. Additionally, for 10.x, you can install it using pip:

```
pip3 install asciidoc
```

## Tools

Current AsciiDoc version tested on Ubuntu 18.04 with:

- Python 3.6.5
- DocBook XSL Stylesheets 1.76.1
- xsltproc (libxml 20706, libxslt 10126 and libexslt 815).
- w3m 0.5.2
- dblatex 0.3
- FOP 0.95

## Copying

Copyright (C) 2002-2013 Stuart Rackham.  
Copyright (C) 2013-2021 AsciiDoc Contributors.

Free use of this software is granted under the terms of the GNU General
Public License version 2 (GPLv2).
