# using run-workflow.sh with PostgreSQL
To run a workflow using the main bash script and PostgreSQL, run the following in the root repository folder (i.e., the `crossfilter-benchmark-eval` root folder):
```
./run-workflow.sh [env folder location] [dataset] postgresql [workflow]
```

Example:
```
./run-workflow.sh ../env movies postgresql 8862a0ca-295b-42b6-acb6-840a53128b62_movies_3_workflow_fixed
```

NOTE: this script assumes you are using a virtual environment to run Python with IDEBench. "env folder location" refers to the location of the Python virtual environment setup for running IDEBench.

NOTE: this assumes someone already went through the trouble of setting up PostgreSQL separately (these scripts will not setup postgresql for you!)

NOTE: this does not finally stop the database! this step should be handled either manually or using a larger script that processes multiple workflows...

# Using the PostgreSQL scripts
There is a bash script saved in this folder (`setup/postgresql`) for basic things that need to be done with Postgresql. To run any of these scripts, simply run them directly in the root folder of this repository:
```
./setup/postgresql/[scriptname].sh
```

For example, to start the crossfilter database:
```
./setup/postgresql/start-database.sh
```

To run the experiments with IDEBench and PostgreSQL, you will need the PostgreSQL Python connector: `psycopg2`.

An example of how to run experiments using PostgreSQL with the benchmark (using the root repository folder):
```
python idebench.py --settings-dataset movies --settings-size 1GB --driver-name postgresql --run --settings-workflow 8862a0ca-295b-42b6-acb6-840a53128b62_movies_3_workflow_fixed
```

# Experiment flow
In general, all of the following steps should be carried out to have a clean run with PostgreSQL. The following sections explains each of the scripts.
1. start the database (using `start-database.sh`)
2. load the data for the desired dataset sizes (e.g., for 1M dataset size, use `load_1M.sh`)
3. for each workflow:
    1. stop the database (using `stop-database.sh`)
    2. start the database (using `start-database.sh`)
    3. run IDEBench for the given workflow
4. stop the database one final time (using `stop-database.sh`)

Note that steps 1 and 4 just need to be done once before and after all the experiments are run, respectively.

# Starting and Stopping the PostgreSQL Service
You can start the PostgreSQL service using `start-database.sh`:
```
./setup/postgresql/start-database.sh
```

To stop the PostgreSQL service after running experiments, we can use `stop-database.sh`:
```
./setup/postgresql/stop-database.sh
```

# Creating the Crossfilter user
The experiments use a specific PostgreSQL user called "crossfilter" to manage the database tables. If this user does not yet exist, you can create this user, using the `create-user.sh` script:
```
./setup/postgresql/create-user.sh
```

# Loading Datasets
To make it easy and fast to load the datasets for a given dataset size, we have created a separate script to load all three datasets (flights, movies, weather) for the different dataset sizes (1M, 10M, 100M records). For example, to load the 1M dataset size of all datasets, use the `load_1M.sh` script:
```
./setup/postgresql/load_1M.sh
```
