#!/bin/bash

# uses crossfilter user credentials
postgres_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )/../postgresql" >/dev/null 2>&1 && pwd )"
${postgres_dir}/./load_10M.sh

python setup/verdictdb/createScrambles.py
