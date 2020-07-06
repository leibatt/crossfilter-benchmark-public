#!/bin/bash

SOURCE="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
for DBMS in $( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && ls -d */ )
do
  if [ "$DBMS" != "verdictdb/" ]; then # verdictdb just uses postgresql
    echo ${SOURCE}/${DBMS}./stop-database.sh
    ${SOURCE}/${DBMS}./stop-database.sh
  fi
done

#postgres_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )/../postgresql" >/dev/null 2>&1 && pwd )"
