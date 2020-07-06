#!/bin/bash

#data/flights/workflows

if [ "$#" -ne 5 ]; then
  echo "You must enter exactly 5 command line arguments"
  echo "Usage: ./run-workflows-for-dataset.sh [env folder location] [dataset size] [dataset] [driver] [run folder name]"
  echo "Example: ./run-workflows-for-dataset.sh ../env 1M movies monetdb results/run_1"
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
# to keep track of which run it was
RUN_FOLDERNAME=$5

# to store results for this specific case
RESULT_DESTINATION="${RUN_FOLDERNAME}/size_${DATASET_SIZE}/${DATASET}/${DRIVER}"

# make the result destination
echo "preparing result destination folders: ${RESULT_DESTINATION}"
mkdir -p ${RESULT_DESTINATION}

if [ "${DATASET}" = "flights" ]; then
  for WORKFLOW_FILENAME in $( ls data/${DATASET}/workflows )
  do
    if [ -f "stop_scripts" ]; then
      echo "stopping execution run-workflows-for-dataset.sh"
      exit 0
    fi

    WORKFLOW="${WORKFLOW_FILENAME%.*}"
    echo "./run-workflow.sh ${ENVIR_FOLDER} ${DATASET_SIZE} ${DATASET} ${DRIVER} ${WORKFLOW} ${RESULT_DESTINATION}"
    ./run-workflow.sh ${ENVIR_FOLDER} ${DATASET_SIZE} ${DATASET} ${DRIVER} ${WORKFLOW} ${RESULT_DESTINATION}
  done
elif [ "${DATASET}" = "movies" ]; then
  for WORKFLOW_FILENAME in $( ls data/${DATASET}/workflows/ | grep ".*_fixed.json" )
  do
    if [ -f "stop_scripts" ]; then
      echo "stopping execution run-workflows-for-dataset.sh"
      exit 0
    fi

    WORKFLOW="${WORKFLOW_FILENAME%.*}"
    echo "./run-workflow.sh ${ENVIR_FOLDER} ${DATASET_SIZE} ${DATASET} ${DRIVER} ${WORKFLOW} ${RESULT_DESTINATION}"
    ./run-workflow.sh ${ENVIR_FOLDER} ${DATASET_SIZE} ${DATASET} ${DRIVER} ${WORKFLOW} ${RESULT_DESTINATION}
  done
elif [ "${DATASET}" = "weather" ]; then
  for WORKFLOW_FILENAME in $( ls data/${DATASET}/workflows )
  do
    if [ -f "stop_scripts" ]; then
      echo "stopping execution of run-workflows-for-dataset.sh"
      exit 0
    fi

    WORKFLOW="${WORKFLOW_FILENAME%.*}"
    echo "./run-workflow.sh ${ENVIR_FOLDER} ${DATASET_SIZE} ${DATASET} ${DRIVER} ${WORKFLOW} ${RESULT_DESTINATION}"
    ./run-workflow.sh ${ENVIR_FOLDER} ${DATASET_SIZE} ${DATASET} ${DRIVER} ${WORKFLOW} ${RESULT_DESTINATION}
  done
else
  echo "You must enter valid dataset name."
  echo "Example: ./run-workflows-for-dataset.sh ../env movies monetdb"
  exit 0
fi

