import json
import datetime, time
import itertools
import pyverdict
import decimal
import os
import multiprocessing
from multiprocessing import Queue
from common import util
import pandas as pd
import numpy as np
import queue
import threading
from threading import Thread

#logger = logging.getLogger("idebench")
class IDEBenchDriver:

    # def init(self, options, schema, driver_arg):
    #     pass
    #
    # def workflow_start(self):
    #     print("workflow start")
    #     pass
    #
    # def workflow_end(self):
    #     #os.system("/usr/local/pgsql/bin/pg_ctl stop -D ~/xdb_data")
    #     #os.system('sudo -b bash -c "echo 1 > /proc/sys/vm/drop_caches"')
    #     #os.system("/usr/local/pgsql/bin/pg_ctl start -D ~/xdb_data")
    #     pass

    #def can_execute_online(self, sql_statement):
    #    return (not " or " in sql_statement.lower()) and (not " AVG(" in sql_statement)

    def verdictdbedit(self, sql_statement):
        sql_statement=sql_statement.replace('FROM movies','FROM public.movies_scrambled_'+str(self.verdictdbconfig["scramblePercent"])+'_percent')
        sql_statement=sql_statement.replace('FROM flights','FROM public.flights_scrambled_'+str(self.verdictdbconfig["scramblePercent"])+'_percent')
        sql_statement=sql_statement.replace('FROM weather','FROM public.weather_scrambled_'+str(self.verdictdbconfig["scramblePercent"])+'_percent')
        #print("SQL:",sql_statement)
        return sql_statement.lower()

    def create_connection(self):
        connection = pyverdict.postgres(host=self.config['host'], user='crossfilter', password=self.config['password'], port=self.config['port'], dbname='crossfilter-eval-db')
        connection.set_loglevel("ERROR")
        return connection

    def init(self, options, schema, driver_arg):
        self.time_of_latest_request = 0
        self.isRunning = False
        self.requests = queue.LifoQueue()
        with open("verdictdb.config.json","r") as f:
          self.verdictdbconfig = json.load(f)
        self.config = json.load(open(os.path.join(os.path.dirname(__file__),'..','verdictdb.config.json')))

    def execute_vizrequest(self, viz_request, options, schema, result_queue):

        viz = viz_request.viz
        sql_statement = viz.get_computed_filter_as_sql(schema)
        #calculate connection time

        # get a connection from the pool - block if non is available
        # connection = self.pool.get()
        connection=self.conn

        viz_request.start_time = util.get_current_ms_time()
        try:
            editedSqlStatement = self.verdictdbedit(sql_statement)
            #print(editedSqlStatement)
            data = connection.sql(editedSqlStatement)
        except Exception as e:
            print(e, flush=True)
            viz_request.result = {}
            viz_request.margins = {}
            viz_request.end_time = util.get_current_ms_time()
            result_queue.put(viz_request)
            return
        viz_request.end_time = util.get_current_ms_time()


        # put connection back in the queue so the next thread can use it.
        #cursor.close()
        #connection.close()
        #connection=self.create_connection()
        #self.pool.put(connection)

        results = {}
        for i, row in data.iterrows():
            keys = []
            if row[0] is None:
                continue
            for i, bin_desc in enumerate(viz_request.viz.binning):
                if "width" in bin_desc:
                    bin_width = bin_desc["width"]
                    keys.append(str(int(row[0])))
                else:
                    keys.append(str(row[0]).strip())
            key = ",".join(keys)
            row = list(row)
            for i, r in enumerate(row):
                if isinstance(r, decimal.Decimal):
                    row[i] = float(r)
            results[key] = row[1]
        viz_request.result = results
        #viz_request.margins = margins
        viz_request.margins = {}
        result_queue.put(viz_request)
        print("delivering...")

    def process_request(self, viz_request, options, schema, result_queue):
        self.requests.put((viz_request, options, schema, result_queue))

    def process(self):
        # while the workflow is running, pop the latest request from the stack and execute it
        while self.isRunning:
            try:
                request = self.requests.get(timeout=1)
                viz_request = request[0]
                options = request[1]
                schema = request[2]
                result_queue = request[3]


                # only execute requests that are newer than the last one we processed (drops old/no longer needed queries)
                if viz_request.expected_start_time < self.time_of_latest_request:
                    viz_request.dropped = True
                    result_queue.put(viz_request)
                    continue

                self.time_of_latest_request = viz_request.expected_start_time
                self.execute_vizrequest(viz_request, options, schema, result_queue)
            except Exception as e:
                # ignore queue-empty exceptions
                print(e, flush=True)
                pass
        self.conn.close()

    def workflow_start(self):
         # pool a number of db connections
        self.isRunning = True
        #self.pool = queue.Queue()
        #for i in range(1):
        #    conn = self.create_connection()
        #    self.pool.put(conn)

        self.conn=self.create_connection()
        thread = Thread(target = self.process)
        thread.start()

    def workflow_end(self):
        self.isRunning = False
        # close all db connections at the end of a workflow
        #for i in range(self.pool.qsize()):
        #    conn = self.pool.get(timeout=1)
        #    conn.close()
    # def process_request(self, viz_request, options, schema, out_q):
    #     print("processsing..." + str(viz_request.operation_id))
    #     if viz_request.viz.binning:
    #         sql_statement = viz_request.viz.get_computed_filter_as_sql(schema)
    #         sql_statement = sql_statement.replace(schema.get_fact_table_name(), "%s_%s%s" % (
    #         schema.get_fact_table_name(), options.settings_size, "n" if options.settings_normalized else ""))
    #         #if self.can_execute_online(sql_statement):
    #         #    sql_statement = sql_statement.replace("SELECT ", "SELECT ONLINE ")
    #         #    sql_statement += " WITHTIME %s CONFIDENCE 95" % options.settings_time_requirement
    #         #    sql_statement += " REPORTINTERVAL %s;" % options.settings_time_requirement
    #         #    connection, cursor = self.create_connection(options.settings_time_requirement + 20)
    #
    #         #connection, cursor = self.create_connection(options.settings_time_requirement)
    #         #calculate connection time
    #         t1=util.get_current_ms_time()
    #         connection, cursor = self.create_connection()
    #         t2=util.get_current_ms_time()
    #         viz_request.connection_time=t2-t1
    #         viz_request.start_time = util.get_current_ms_time()
    #         try:
    #             data = connection.sql(self.verdictdbedit(sql_statement))
    #         except:
    #             viz_request.result = {}
    #             viz_request.margins = {}
    #             viz_request.timedout = True
    #             viz_request.end_time = util.get_current_ms_time()
    #             out_q.put(viz_request)
    #             return
    #         #data = connection.sql(self.verdictdbedit(sql_statement))
    #         #data=connection.sql(sql_statement)
    #
    #         viz_request.end_time = util.get_current_ms_time()
    #         connection.close()
    #
    #         results = {}
    #         margins = {}
