#!/usr/bin/env bash

cat > MANIFEST.tmp <<- EOM
asciidoc/*.py
asciidoc/**/*.py
asciidoc/resources/**/*
asciidoc/resources/*.conf
doc/asciidoc.conf
doc/article-docinfo.xml
doc/customers.csv
doc/*.1
doc/*.txt
doc/asciidoc.dict
images/*
tests/data/*
tests/inputs/*
tests/*.py
tests/testasciidoc.conf
*.sh
BUGS.adoc
CHANGELOG.adoc
configure.ac
COPYRIGHT
Dockerfile
install-sh
INSTALL.adoc
LICENSE
MANIFEST.in
Makefile.in
README.md
setup.py
EOM

rm -f MANIFEST
while read in; do
    if [ ! -z "${in}" ]; then
        ls -1Ad ${in} | grep -v ".pyc" | grep -v "__pycache__" >> MANIFEST
    fi
done < MANIFEST.tmp
echo "MANIFEST" >> MANIFEST
rm -f MANIFEST.tmp
