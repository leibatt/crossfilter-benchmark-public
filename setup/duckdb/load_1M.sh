#!/bin/bash

root_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )/../.." >/dev/null 2>&1 && pwd )"
current_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
# locate the monetdb configuration file
duckdb_config="${root_dir}/duckdb.config.json"
# get the location to put the dbfarm
dbFilename=`python -c "import sys, json; print(json.load(open(\"${duckdb_config}\"))['dbFilename'])"`
rm $dbFilename

# will make the database in the current folder
#python setup/duckdb/load_1M.py "${root_dir}/crossfilter-eval-db.duckdb"
python ${current_dir}/load_1M.py
