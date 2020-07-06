#!/bin/bash

current_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
root_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )/../.." >/dev/null 2>&1 && pwd )"
# uses monetdb user credentials
export DOTMONETDBFILE="${current_dir}/.monetdb"

# create the tables
mclient -d crossfilter-eval-db < ${current_dir}/createFlights.sql
mclient -d crossfilter-eval-db < ${current_dir}/createMovies.sql
mclient -d crossfilter-eval-db < ${current_dir}/createWeather.sql

# load the data
mclient -d crossfilter-eval-db  -s "COPY 1000000 OFFSET 2 RECORDS INTO sys.flights from '${root_dir}/dataset_flights_1M.csv' DELIMITERS ',';"
mclient -d crossfilter-eval-db  -s "COPY 1000000 OFFSET 2 RECORDS INTO sys.movies from '${root_dir}/dataset_movies_1M_fixed.csv' DELIMITERS ',';"
mclient -d crossfilter-eval-db  -s "COPY 1000000 OFFSET 2 RECORDS INTO sys.weather from '${root_dir}/dataset_weather_1M_fixed.csv' DELIMITERS ',';"

# setup the crossfilter user
mclient -d crossfilter-eval-db < ${current_dir}/setupUser.sql
