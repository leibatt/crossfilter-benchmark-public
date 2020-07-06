#!/bin/bash

current_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
${current_dir}/./stop-database.sh
${current_dir}/./remove-database.sh
${current_dir}/./create-database.sh
${current_dir}/./start-database.sh
