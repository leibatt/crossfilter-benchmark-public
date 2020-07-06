# using run-workflow.sh with MonetDB
To run a workflow using the main bash script and MonetDB, run the following in the root repository folder (i.e., the `crossfilter-benchmark-eval` root folder):
```
./run-workflow.sh [env folder location] [dataset] monetdb [workflow]
```

Example:
```
./run-workflow.sh ../env movies monetdb 8862a0ca-295b-42b6-acb6-840a53128b62_movies_3_workflow_fixed
```

NOTE: this script assumes you are using a virtual environment to run Python with IDEBench. "env folder location" refers to the location of the Python virtual environment setup for running IDEBench.

NOTE: this does not start and stop the dbfarm, and it does not finally stop the database! these steps should be handled either manually or using a larger script that processes multiple workflows...

# Using the MonetDB scripts
There is a bash script saved in this folder (`setup/monetdb`) for anything that needs to be done with MonetDB. To run any of these scripts, simply run them directly in the root folder of this repository:
```
./setup/monetdb/[scriptname].sh
```

For example, to reset the crossfilter database (assuming the dbfarm has been created already):
```
./setup/monetdb/reset-database.sh
```

To run the experiments with IDEBench and MonetDB, you will need the MonetDB Python connector: `pymonetdb`.

An example of how to run experiments using MonetDB with the benchmark (using the root repository folder):
```
python idebench.py --settings-dataset movies --settings-size 1GB --driver-name monetdb --run --settings-workflow 8862a0ca-295b-42b6-acb6-840a53128b62_movies_3_workflow_fixed
```

# Experiment flow
In general, all of the following steps should be carried out to have a clean run with MonetDB. These steps assume that the dbfarm has already been created. The following sections explains each of the scripts.
1. start the dbfarm (using `start-dbfarm.sh`)
2. reset the database (using `reset-database.sh`)
3. load the data for the desired dataset sizes (e.g., for 1M dataset size, use `load_1M.sh`)
4. for each workflow:
    1. stop the database (using `stop-database.sh`)
    2. start the database (using `start-database.sh`)
    3. run IDEBench for the given workflow
5. stop the database one final time (using `stop-database.sh`)
6. stop the dbfarm (using `stop-dbfarm.sh`)

Note that steps 1 and 2 just need to be performed once before all experiments, and steps 5 and 6 once after all experiments are done.

# Starting, Stopping (and if necessary Creating) the MonetDB DBFarm
MonetDB needs a dbfarm first, to manage multiple databases. If you need to create one, this can be done using the `create-dbfarm.sh` script, which will create the dbfarm:
```
./setup/monetdb/create-dbfarm.sh
```

After creating the dbfarm, then you need to start it, which you can use the `start-dbfarm.sh` script:
```
./setup/monetdb/start-dbfarm.sh
```

After running expeirments, you need to stop the dbfarm using the `stop-dbfarm.sh` script:
```
./setup/monetdb/stop-dbfarm.sh
```

# Setting Up, Starting, and Stopping the Crossfilter Database
Once the dbfarm is up and running, then we need a database to run experiments with. You can create the crossfilter database using the `create-database.sh` script:
```
./setup/monetdb/create-database.sh
```

Once we have the database, we can start it using `start-database.sh`:
```
./setup/monetdb/start-database.sh
```

As a shortcut, you can quickly re-create the database from scratch using the `reset-database.sh`:
```
./setup/monetdb/reset-database.sh
```

To stop the database after running experiments, we can use `stop-database.sh`:
```
./setup/monetdb/stop-database.sh
```

# Loading Datasets
To make it easy and fast to load the datasets for a given dataset size, we have created a separate script to load all three datasets (flights, movies, weather) for the different dataset sizes (1M, 10M, 100M records). For example, to load the 1M dataset size of all datasets, use the `load_1M.sh` script:
```
./setup/monetdb/load_1M.sh
```
