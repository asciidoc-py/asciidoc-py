#!/usr/bin/env python3

import os
from os import path
import glob


def sort_files(files):
    return sorted(files, key=lambda v: v.lower())


def get_files(basedir):
    return_files = []

    entries = os.listdir(basedir)
    files = sort_files(
        filter(
            lambda x: path.isfile(path.join(basedir, x)) and not x.endswith('.pyc'),
            entries
        ),
    )
    dirs = sort_files(
        filter(
            lambda x: path.isdir(path.join(basedir, x)) and
            (x != '__pycache__' or
                '.gitkeep' in os.listdir(path.join(basedir, x))),
            entries,
        )
    )
    for dir in dirs:
        return_files += get_files(path.join(basedir, dir))
    return_files += [path.join(basedir, f) for f in files]
    return return_files


manifest_list = []

manifest_list += get_files('asciidoc')

doc_glob = [
    'doc/*.1',
    'doc/*.txt',
]

doc_files = [
    'doc/article-docinfo.xml',
    'doc/asciidoc.conf',
    'doc/asciidoc.dict',
    'doc/customers.csv',
]

for entry in doc_glob:
    doc_files += glob.glob(entry)

manifest_list += sort_files(doc_files)

manifest_list += sort_files(glob.glob('images/*'))

manifest_list += get_files('tests')

manifest_list += sort_files([
    'BUGS.adoc',
    'build_manifest.py',
    'CHANGELOG.adoc',
    'configure.ac',
    'COPYRIGHT',
    'Dockerfile',
    'install-sh',
    'INSTALL.adoc',
    'LICENSE',
    'Makefile.in',
    'MANIFEST',
    'MANIFEST.in',
    'README.md',
    'setup.py',
])

with open('MANIFEST', 'w') as open_file:
    open_file.write("\n".join(manifest_list) + "\n")
