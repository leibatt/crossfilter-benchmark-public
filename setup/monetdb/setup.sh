#!/bin/bash

current_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
## if dbfarm is not created, uncomment and execute:
#./${current_dir}/create-dbfarm.sh
#./${current_dir}/start-dbfarm.sh

# create and start the database
${current_dir}/./create-database.sh
${current_dir}/./start-database.sh
