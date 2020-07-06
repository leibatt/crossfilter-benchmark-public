#!/bin/bash

if [ "$#" -ne 1 ]; then
  echo "You must specify python virtual environment directory"
  echo "Usage: ./run-all-workflows-all-drivers.sh [env folder location]"
  echo "Example: ./run-all-workflows-all-drivers.sh ../env"
  exit 0
fi

# the virtual environment to use
ENVIR_FOLDER=$1

#nicely formatted timestamp
RUN_TIMESTAMP=$(date +%m-%d-%y_%T)
RUN_FOLDERNAME="results/run_${RUN_TIMESTAMP}"
DUCKDB_INSTALL_FOLDER="duckdb_install"
LOGFILE="${RUN_FOLDERNAME}/output.txt"

echo "removing any stop_scripts file just in case"
rm stop_scripts

echo "creating run folder ${RUN_FOLDERNAME}"
mkdir -p $RUN_FOLDERNAME

echo "activating environment" >> $LOGFILE 2>&1
source ${ENVIR_FOLDER}/bin/activate >> $LOGFILE 2>&1

echo "downloading duckdb for later local re-installation" >> $LOGFILE 2>&1
mkdir -p $DUCKDB_INSTALL_FOLDER >> $LOGFILE 2>&1
rm $DUCKDB_INSTALL_FOLDER/* >> $LOGFILE 2>&1
for ATTEMPT_ID in 1 2 3 4 5 6 7 8 9 10
do
  pip download -d $DUCKDB_INSTALL_FOLDER duckdb >> $LOGFILE 2>&1
  contents=$(ls $DUCKDB_INSTALL_FOLDER | grep "duckdb.*\.whl" | wc -l)
  echo "contents $contents" >> $LOGFILE 2>&1
  if [ "$contents" -gt "0" ]; then
    break
  fi
done
echo "successfully downloaded duckdb locally" >> $LOGFILE 2>&1

echo "deactivating environment" >> $LOGFILE 2>&1
deactivate >> $LOGFILE 2>&1

#for DATASET_SIZE in "1M" "10M" "100M"
for DATASET_SIZE in "1M"
do

  echo "stopping all DBMSs" >> $LOGFILE 2>&1
  setup/./stop-all.sh >> $LOGFILE 2>&1
  echo "starting all DBMSs" >> $LOGFILE 2>&1
  setup/./start-all.sh >> $LOGFILE 2>&1

  echo "activating environment" >> $LOGFILE 2>&1
  source ${ENVIR_FOLDER}/bin/activate >> $LOGFILE 2>&1

  if [ -f "stop_scripts" ]; then
    echo "stopping execution of run-all-workflows-all-drivers.sh" >> $LOGFILE 2>&1
    deactivate
    exit 0
  fi

  echo "loading datasets for size ${DATASET_SIZE} into all DBMSs" >> $LOGFILE 2>&1
  setup/./load-${DATASET_SIZE}-all.sh >> $LOGFILE 2>&1

  if [ -f "stop_scripts" ]; then
    echo "stopping execution of run-all-workflows-all-drivers.sh" >> $LOGFILE 2>&1
    deactivate
    exit 0
  fi

  echo "deactivating environment" >> $LOGFILE 2>&1
  deactivate >> $LOGFILE 2>&1

  for DATASET in "weather" "movies" "flights"
  do
    for SCRAMBLE_PERCENT in 10 50
    do
      DRIVER="verdictdb"
      echo "eventually saving to ${RUN_FOLDERNAME}/size_${DATASET_SIZE}/${DATASET}/${DRIVER}-${SCRAMBLE_PERCENT}" >> $LOGFILE 2>&1
      #echo '{"scramblePercent":' ${SCRAMBLE_PERCENT} '}' > verdictdb.config.json
      echo "python -c \"import sys, json; config=json.load(open('verdictdb.config.json')); config['scramblePercent'] = ${SCRAMBLE_PERCENT}; json.dump(config,open('verdictdb.config.json','w')); \""
      python -c "import sys, json; config=json.load(open('verdictdb.config.json')); config['scramblePercent'] = ${SCRAMBLE_PERCENT}; json.dump(config,open('verdictdb.config.json','w'))"
      echo "./run-workflows-for-dataset.sh $ENVIR_FOLDER $DATASET_SIZE $DATASET $DRIVER $RUN_FOLDERNAME >> $LOGFILE" 2>&1
      ./run-workflows-for-dataset.sh $ENVIR_FOLDER $DATASET_SIZE $DATASET $DRIVER $RUN_FOLDERNAME >> $LOGFILE 2>&1
    
      if [ -f "stop_scripts" ]; then
        echo "stopping execution of run-all-workflows-all-drivers.sh" >> $LOGFILE 2>&1
        exit 0
      fi
      
      echo "mv ${RUN_FOLDERNAME}/size_${DATASET_SIZE}/${DATASET}/${DRIVER} ${RUN_FOLDERNAME}/size_${DATASET_SIZE}/${DATASET}/${DRIVER}-${SCRAMBLE_PERCENT}" >> $LOGFILE 2>&1
      mv ${RUN_FOLDERNAME}/size_${DATASET_SIZE}/${DATASET}/${DRIVER} ${RUN_FOLDERNAME}/size_${DATASET_SIZE}/${DATASET}/${DRIVER}-${SCRAMBLE_PERCENT} >> $LOGFILE 2>&1
    done

    for DRIVER in "postgresql" "sqlite" "monetdb" "duckdb"
    do

      echo "./run-workflows-for-dataset.sh $ENVIR_FOLDER $DATASET_SIZE $DATASET $DRIVER $RUN_FOLDERNAME >> $LOGFILE" 2>&1
      ./run-workflows-for-dataset.sh $ENVIR_FOLDER $DATASET_SIZE $DATASET $DRIVER $RUN_FOLDERNAME >> $LOGFILE 2>&1

      if [ -f "stop_scripts" ]; then
        echo "stopping execution of run-all-workflows-all-drivers.sh" >> $LOGFILE 2>&1
        exit 0
      fi
    done
  done
done

