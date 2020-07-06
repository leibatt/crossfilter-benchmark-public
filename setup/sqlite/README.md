# using run-workflow.sh with SQLite
To run a workflow using the main bash script and SQLite, run the following in the root repository folder (i.e., the `crossfilter-benchmark-eval` root folder):
```
./run-workflow.sh [env folder location] [dataset] sqlite [workflow]
```

Example:
```
./run-workflow.sh ../env movies sqlite 8862a0ca-295b-42b6-acb6-840a53128b62_movies_3_workflow_fixed
```

NOTE: this script assumes you are using a virtual environment to run Python with IDEBench. "env folder location" refers to the location of the Python virtual environment setup for running IDEBench.

NOTE: resetting the SQLite database using the setup script requires Pandas, so your Python virtual environment will need to import `pandas` and `sqlite3`

NOTE: starting/stopping the database doesn't actually do anything with SQLite, so you can ignore these scripts (included just so the execution flow is consistent for the `run-workflow.sh` script).

# Using the SQLite scripts
There is a bash script saved in this folder (`setup/sqlite`) for basic things that need to be done for SQLite. To run any of these scripts, simply run them directly in the root folder of the crossfilter-benchmark-eval repository:
```
./setup/sqlite/[scriptname].sh
```

To run the experiments with IDEBench and SQLite, you will need the `sqlite3` Python connector.

An example of how to run experiments using SQLite with the benchmark using IDEBench directly (using the root repository folder):
```
python idebench.py --settings-dataset movies --settings-size 1GB --driver-name sqlite --run --settings-workflow 8862a0ca-295b-42b6-acb6-840a53128b62_movies_3_workflow_fixed
```

# Experiment flow
In general, all of the following steps should be carried out to have a clean run with SQLite. The following sections explains each of the scripts.
1. for each workflow:
    * run IDEBench for the given workflow

Note that SQLite doesn't have any setup/teardown requirements, so we do not have to do start/stop of the database. These scripts only exist for consistency's sake.

# Refreshing the SQLite Databaes and Reloading Datasets
To make it easy and fast to load the datasets for a given dataset size, we have created a separate script to load all three datasets (flights, movies, weather) for the different dataset sizes (1M, 10M, 100M records). For example, to load the 1M dataset size of all datasets, use the `load_1M.sh` script:
```
setup/sqlite/./load_1M.sh
```
