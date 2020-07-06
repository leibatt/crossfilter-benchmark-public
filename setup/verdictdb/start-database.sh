#!/bin/bash

# start postgresql
postgres_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )/../postgresql" >/dev/null 2>&1 && pwd )"
${postgres_dir}/./start-database.sh
