#!/bin/bash

filename="ArangoDB.tgz"

function build {
    python arango_dash.py
    tar -zcvf "${filename}" "ArangoDB.docset"
}

if [ -f "${filename}" ]; then
    echo "removing file"
    rm "${filename}"
    build
else
    build
fi