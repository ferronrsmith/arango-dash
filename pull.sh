#!/bin/bash

arango_site="docs.arangodb.com"

archives=("ArangoDB-Cookbook" "ArangoDB")

# function build {
#     python arango_dash.py -t "${1}"
#     tar -zcvf "${1}.tgz" "${1}.docset"
# }


function process {
	for archive in "${archives[@]}"
	do
	    if [ -f "${archive}" ]; then
	        echo "removing file"
	        rm "${archive}"
	        struct "${archive}"
	    else
	        struct "${archive}"
	    fi
	done	
}

function struct {
	local location="${1}.docset/Contents/Resources/Documents/${arango_site}"
	find "${location}/" -mindepth 1 -exec rm -rf {} \; 2> /dev/null
	if [ "${1}" == "ArangoDB-Cookbook" ]; then
		echo "writing cookbook to ${location}"
		cp -R "${arango_site}/cookbook"/* "${location}"
	elif [[ "${1}" == "ArangoDB" ]]; then
		echo "writing docs to ${location}"
		rm -rf "${arango_site}/cookbook"
		cp -R "${arango_site}"/* "${location}"
	fi
}

function clean {
	rm -rf "${arango_site}"
}

function tar_arc {
	local dt
	dt=$(date +"%Y-%m-%d")
	if [ ! -f "${arango_site}-${dt}.tgz" ]; then
		tar -zcvf "${arango_site}-${dt}.tgz" "${arango_site}"
	else
		echo "already archived"
	fi
}

function proc {
	if [ -d "${arango_site}" ]; then
		# pulling website
		tar_arc
		process
	else
		wget -r https://docs.arangodb.com/
		tar_arc
		process
	fi
}

val="$1"

if [ -z "${val}" ]; then
	proc	
elif [ "${val}" == "c" ]; then
	clean
  proc
fi
