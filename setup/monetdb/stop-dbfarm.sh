#!/bin/bash

# locate the root directory
root_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )/../.." >/dev/null 2>&1 && pwd )"
# locate the monetdb configuration file
monetdb_config="${root_dir}/monetdb.config.json"
# get the location to put the dbfarm
dbfarm_location=`python -c "import sys, json; print(json.load(open(\"${monetdb_config}\"))['dbfarm-location'])"`
# stop db farm
monetdbd stop $dbfarm_location
