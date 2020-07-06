#!/bin/bash

current_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
export DOTMONETDBFILE="${current_dir}/.monetdb"
mclient -d crossfilter-eval-db < ${current_dir}/setupUser.sql
