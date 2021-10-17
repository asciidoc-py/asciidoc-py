#!/usr/bin/env bash

cat > MANIFEST.tmp <<- EOM
asciidoc/*.py
asciidoc/**/*
doc/asciidoc.conf
doc/article-docinfo.xml
doc/customers.csv
doc/*.1
doc/*.txt
doc/asciidoc.dict
tests/data/*
tests/testasciidoc.py
tests/testasciidoc.conf
*.sh
BUGS.txt
CHANGELOG.txt
configure
configure.ac
COPYRIGHT
Dockerfile
MANIFEST
MANIFEST.in
install-sh
INSTALL.txt
Makefile
Makefile.in
README.md
EOM

rm -f MANIFEST
while read in; do
    if [ ! -z "${in}" ]; then
        ls -1Ad ${in} | grep -v ".pyc" | grep -v "__pycache__" >> MANIFEST
    fi
done < MANIFEST.tmp
echo "MANIFEST" >> MANIFEST
rm -f MANIFEST.tmp
