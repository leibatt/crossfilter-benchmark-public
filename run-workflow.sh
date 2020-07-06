#!/bin/bash


if [ "$#" -ne 6 ]; then
  echo "You must enter exactly 6 command line arguments"
  echo "Usage: ./run-workflow.sh [env folder location] [dataset size] [dataset] [driver] [workflow] [result destination]"
  echo "Example: ./run-workflow.sh ../env 1M movies monetdb 8862a0ca-295b-42b6-acb6-840a53128b62_movies_3_workflow_fixed results/test"
  exit 0
fi

#set -x

# the virtual environment to use
ENVIR_FOLDER=$1
#dataset size
DATASET_SIZE=$2
# which dataset to test
DATASET=$3
# which database driver to test
DRIVER=$4
# which workflow to test
WORKFLOW=$5
# where to move the result to
RESULT_DESTINATION=$6
# where DuckDB files are located
DUCKDB_INSTALL_FOLDER="duckdb_install"

if [ -f "stop_scripts" ]; then
  echo "stopping execution of run-workflow.sh"
  exit 0
fi

# clear the results folder
echo "clearing the results folder"
rm results/*.json

# activate the environment
echo "activating environment"
source ${ENVIR_FOLDER}/bin/activate

# worst case, it will attempt to run the current workflow 20 times
for ATTEMPT_ID in 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20
do

  if [ -f "stop_scripts" ]; then
    echo "stopping execution of run-workflow.sh"
    exit 0
  fi

  echo "attempt ${ATTEMPT_ID}"

  # stop the database
  echo "stopping database ${DRIVER}"
  ./setup/${DRIVER}/stop-database.sh

  # start the database
  echo "starting database ${DRIVER}"
  ./setup/${DRIVER}/start-database.sh

  # duckdb will end up in an inconsistent state if we continuously
  # reuse the same database. to play it safe with duckdb,
  #  just refresh every time. Slow, but dependable.
  # UPDATE 10/05/2019: we really need this!!! do not comment out!
  if [ "${DRIVER}" = "duckdb" ] && [ "${ATTEMPT_ID}" -gt "1" ]; then
    echo "pip uninstall -y duckdb"
    pip uninstall -y duckdb

    echo "pip install --find-links $DUCKDB_INSTALL_FOLDER duckdb"
    pip install --find-links $DUCKDB_INSTALL_FOLDER duckdb

    echo "rm crossfilter-eval-db.duckdb.wal"
    rm crossfilter-eval-db.duckdb.wal

    echo "rm crossfilter-eval-db.duckdb"
    rm crossfilter-eval-db.duckdb

    echo "setup/${DRIVER}/./load_${DATASET_SIZE}.sh"
    setup/${DRIVER}/./load_${DATASET_SIZE}.sh
  fi

  # run IDEBench in the background
  echo "python idebench.py --settings-dataset $DATASET --settings-size 1GB --driver-name $DRIVER --run --settings-workflow $WORKFLOW &"
  python idebench.py --settings-dataset $DATASET --settings-size 1GB --driver-name $DRIVER --run --settings-workflow $WORKFLOW & pid=$!

  # check if it's still running in the background
  STILL_RUNNING=$(jobs -p | grep $pid | wc -l)

  # check the number of results produced
  TOTAL_RESULTS=$(ls results | grep ".*.json" | wc -l)

  # wait for the process to finish
  while true
  do

    if [ -f "stop_scripts" ]; then
      echo "stopping execution of run-workflow.sh"
      kill $pid
      exit 0
    fi

    echo "checking status of job $pid"
    # check if it's still running in the background
    STILL_RUNNING=$(jobs -p | grep $pid | wc -l)
    # check the number of results produced
    TOTAL_RESULTS=$(ls results | grep ".*.json" | wc -l)
    if [ -f "restart_job" ]; then
      echo "restarting execution of run-workflow.sh"
      STILL_RUNNING=0
      TOTAL_RESULTS=0
    fi
    echo "status of ${pid}: still running? ${STILL_RUNNING}. total results? ${TOTAL_RESULTS}"

    if [ "$STILL_RUNNING" -eq "0" ]; then
      # it's done already, move on
      break
    elif [ "$TOTAL_RESULTS" -gt "0" ]; then
      # to be sure, give it time to finish gracefully, then try to kill it
      sleep 10
      kill $pid
      break
    else
      # wait 10 seconds
      sleep 10
    fi
  done

  if [ "$TOTAL_RESULTS" -gt "0" ]; then
    echo "found results for attempt ${ATTEMPT_ID}. Continuing on."
    break
  else
    echo "no results found for attempt ${ATTEMPT_ID}. Waiting 10 seconds, then trying again..."
    rm restart_job
    sleep 10 # wait for a bit, then try again
  fi
done

# move results to destination
echo "mv results/*.json ${RESULT_DESTINATION}"
mv results/*.json ${RESULT_DESTINATION}

# deactivate the environment
echo "deactivating environment"
deactivate
