#!/bin/bash

# stop the database
monetdb stop crossfilter-eval-db

# remove the database
monetdb destroy -f crossfilter-eval-db
