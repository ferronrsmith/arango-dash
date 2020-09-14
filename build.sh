#!/bin/bash

archives=("ArangoDB")

function build {
    python arango_dash.py -t "${1}"
    tar -zcvf "${1}.tgz" "${1}.docset"
}

for archive in "${archives[@]}"
do
    if [ -f "${archive}" ]; then
        echo "removing file"
        rm "${archive}"
        build "${archive}"
    else
        build "${archive}"
    fi
done
