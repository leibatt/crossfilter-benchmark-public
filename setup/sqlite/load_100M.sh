#!/bin/bash

root_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )/../.." >/dev/null 2>&1 && pwd )"
current_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
# locate the monetdb configuration file
sqlite_config="${root_dir}/sqlite.config.json"
# get the location to put the dbfarm
dbFilename=`python -c "import sys, json; print(json.load(open(\"${sqlite_config}\"))['dbFilename'])"`
rm $dbFilename

# will make the database in the current folder
#python setup/sqlite/load_100M.py "${root_dir}/crossfilter-eval-db.sqlite"
python ${current_dir}/load_100M.py
