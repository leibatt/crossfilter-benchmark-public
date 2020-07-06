#!/bin/bash

# locate the root directory
root_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )/../.." >/dev/null 2>&1 && pwd )"
# locate the monetdb configuration file
postgres_config="${root_dir}/postgresql.config.json"
# get the location to put the dbfarm
pg_ctl_loc=`python -c "import sys, json; print(json.load(open(\"${postgres_config}\"))['pg_ctl_loc'])"`
data_loc=`python -c "import sys, json; print(json.load(open(\"${postgres_config}\"))['data_loc'])"`
#log_loc=`python -c "import sys, json; print(json.load(open(\"${postgres_config}\"))['log_loc'])"`

# with specified logfile
#$pg_ctl_loc -D $data_loc -l $log_loc start

# without logfile specified
$pg_ctl_loc -D $data_loc start
