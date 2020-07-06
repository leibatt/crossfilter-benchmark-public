#!/bin/bash

postgres_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )/../postgresql" >/dev/null 2>&1 && pwd )"
${postgres_dir}/./create-user.sh
