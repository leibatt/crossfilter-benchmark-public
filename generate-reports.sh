#!/bin/bash

if [ "$#" -ne 2 ]; then
  echo "You must specify python virtual environment directory and evaluation run directory"
  echo "Usage: ./generate-reports.sh [env folder location] [run directory root]"
  echo "Example: ./generate-reports.sh ../env results/run_09-06-19_17\:34\:14/"
  exit 0
fi

# the virtual environment to use
ENVIR_FOLDER=$1
RUN_FOLDERNAME=$2
REPORTS_FOLDERNAME=${RUN_FOLDERNAME/results/reports}

echo "creating reports folder ${REPORTS_FOLDERNAME}"
mkdir -p $REPORTS_FOLDERNAME

generate_report () {
  workflow_loc=$1
  # activate the environment
  echo "activating environment"
  source ${ENVIR_FOLDER}/bin/activate

  # idebench ignores the groundtruth file, pass same file for convenience
  echo "python idebench.py --evaluate=${workflow_loc}"
  python idebench.py --evaluate=${workflow_loc}

  # deactivate the environment
  echo "deactivating environment"
  deactivate
}

calculate_final_results () {
  # activate the environment
  echo "activating environment"
  source ${ENVIR_FOLDER}/bin/activate

  # idebench ignores the groundtruth file, pass same file for convenience
  echo "python analysis/meanduration.py ${REPORTS_FOLDERNAME}"
  python analysis/meanduration.py ${REPORTS_FOLDERNAME}

  # deactivate the environment
  echo "deactivating environment"
  deactivate
}

for size_loc in ${RUN_FOLDERNAME}*/ ; do
    size=$(basename $size_loc)
    #echo "size=${size}"
  for dataset_loc in ${size_loc}*/ ; do
    dataset=$(basename $dataset_loc)
    #echo "dataset=${dataset}"
    for driver_loc in ${dataset_loc}*/ ; do
      driver=$(basename $driver_loc)
      #echo "driver=${driver}"

      # prepare for writing the reports
      report_dest=${driver_loc/results/reports}
      echo "preparing reports destination $report_dest"
      mkdir -p $report_dest

      for workflow_loc in ${driver_loc}* ; do
        workflow=$(basename $workflow_loc)
        #echo "workflow=${workflow}"
        generate_report $workflow_loc
      done

      # move all computed reports to their final location
      echo "moving computed reports to $report_dest"
      mv reports/*.csv $report_dest
    done
  done
done

calculate_final_results
