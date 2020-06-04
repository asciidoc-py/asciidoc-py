#!/usr/bin/env bash

rm -f MANIFEST
while read in; do
    if [ ! -z "${in}" ]; then
        ls -1A ${in} >> MANIFEST
    fi
done < MANIFEST.in
echo "MANIFEST" >> MANIFEST
