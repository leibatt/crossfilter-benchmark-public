#!/bin/bash

# locate the root directory
root_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )/../.." >/dev/null 2>&1 && pwd )"
# locate the monetdb configuration file
postgres_config="${root_dir}/postgresql.config.json"
# get the location to put the dbfarm
psql_loc=`python -c "import sys, json; print(json.load(open(\"${postgres_config}\"))['psql_loc'])"`
password=`python -c "import sys, json; print(json.load(open(\"${postgres_config}\"))['password'])"`
port=`python -c "import sys, json; print(json.load(open(\"${postgres_config}\"))['port'])"`

# uses crossfilter user credentials
export PGPASSWORD=$password
postgres_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )/../postgresql" >/dev/null 2>&1 && pwd )"
$psql_loc -U crossfilter --host=localhost -p $port -d crossfilter-eval-db < ${postgres_dir}/createFlights.sql
$psql_loc -U crossfilter --host=localhost -p $port -d crossfilter-eval-db < ${postgres_dir}/createMovies.sql
$psql_loc -U crossfilter --host=localhost -p $port -d crossfilter-eval-db < ${postgres_dir}/createWeather.sql

$psql_loc -U crossfilter --host=localhost -p $port -d crossfilter-eval-db -c "\\copy weather from '${root_dir}/dataset_weather_10M_fixed.csv' CSV HEADER;"
$psql_loc -U crossfilter --host=localhost -p $port -d crossfilter-eval-db -c "\\copy flights from '${root_dir}/dataset_flights_10M.csv' CSV HEADER;"
$psql_loc -U crossfilter --host=localhost -p $port -d crossfilter-eval-db -c "\\copy movies from '${root_dir}/dataset_movies_10M_fixed.csv' CSV HEADER;"

