import json
import datetime, time
import itertools
import duckdb
import decimal
import os
import multiprocessing
from multiprocessing import Queue
from common import util
import queue
import threading
from threading import Thread


class IDEBenchDriver:

    def init(self, options, schema, driver_arg):
        self.time_of_latest_request = 0
        self.isRunning = False
        self.requests = queue.LifoQueue()
        self.config = json.load(open(os.path.join(os.path.dirname(__file__),'..','duckdb.config.json')))
        

    # def workflow_start(self):
    #     print("workflow start")
    #     pass
    #
    # def workflow_end(self):
    #     #os.system("/usr/local/pgsql/bin/pg_ctl stop -D ~/xdb_data")
    #     #os.system('sudo -b bash -c "echo 1 > /proc/sys/vm/drop_caches"')
    #     #os.system("/usr/local/pgsql/bin/pg_ctl start -D ~/xdb_data")
    #     pass
    #
    # #def can_execute_online(self, sql_statement):
    # #    return (not " or " in sql_statement.lower()) and (not " AVG(" in sql_statement)

    def create_connection(self):
        connection = duckdb.connect(self.config['dbFilename'])
        return connection

    def execute_vizrequest(self, viz_request, options, schema, result_queue):
        viz = viz_request.viz
        sql_statement = viz.get_computed_filter_as_sql(schema)
        #calculate connection time

        # get a connection from the pool - block if non is available
        #connection = self.pool.get()
        connection=self.conn
        cursor = connection.cursor()

        viz_request.start_time = util.get_current_ms_time()
        cursor.execute(sql_statement)
        data = cursor.fetchall()
        viz_request.end_time = util.get_current_ms_time()


        # put connection back in the queue so the next thread can use it.
        cursor.close()
        #self.pool.put(connection)

        results = {}
        for row in data:
            keys = []
            for i, bin_desc in enumerate(viz.binning):

                if "width" in bin_desc:
                    bin_width = bin_desc["width"]
                    keys.append(str(int(row[i])))
                else:
                    keys.append(str(row[i]))

            key = ",".join(keys)
            results[key] = row[len(viz.binning):]

        viz_request.result = results
        result_queue.put(viz_request)

    def process_request(self, viz_request, options, schema, result_queue):
        self.requests.put((viz_request, options, schema, result_queue))

    def process(self):
        self.conn = self.create_connection()
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
                pass
        self.conn.close()

    def workflow_start(self):
         # pool a number of db connections
        self.isRunning = True
        #self.pool = queue.Queue()
        #for i in range(10):
        #    conn = self.create_connection()
        #    self.pool.put(conn)

        thread = Thread(target = self.process)
        thread.start()

    def workflow_end(self):
        self.isRunning = False
        # close all db connections at the end of a workflow
        #for i in range(self.pool.qsize()):
        #    conn = self.pool.get()
        #    conn.close()
        # print("processsing..." + str(viz_request.operation_id))
        # if viz_request.viz.binning:
        #     sql_statement = viz_request.viz.get_computed_filter_as_sql(schema)
        #     sql_statement = sql_statement.replace(schema.get_fact_table_name(), "%s_%s%s" % (
        #     schema.get_fact_table_name(), options.settings_size, "n" if options.settings_normalized else ""))
        #     #if self.can_execute_online(sql_statement):
        #     #    sql_statement = sql_statement.replace("SELECT ", "SELECT ONLINE ")
        #     #    sql_statement += " WITHTIME %s CONFIDENCE 95" % options.settings_time_requirement
        #     #    sql_statement += " REPORTINTERVAL %s;" % options.settings_time_requirement
        #     #    connection, cursor = self.create_connection(options.settings_time_requirement + 20)
        #
        #     #connection, cursor = self.create_connection(options.settings_time_requirement)
        #     #calculate connection time
        #     t1=util.get_current_ms_time()
        #     connection, cursor = self.create_connection()
        #     t2=util.get_current_ms_time()
        #     viz_request.connection_time=t2-t1
        #     viz_request.start_time = util.get_current_ms_time()
        #
        #     cursor.execute(sql_statement)
        #
        #     data = cursor.fetchall()
        #     viz_request.end_time = util.get_current_ms_time()
        #     results = {}
        #     margins = {}
        #     for row in data:
        #         keys = []
        #
        #         if row[0] is None:
        #             continue
        #
        #         #startindex = 3 if self.can_execute_online(sql_statement) else 0
        #         startindex=0
        #         for i, bin_desc in enumerate(viz_request.viz.binning):
        #             if "width" in bin_desc:
        #                 bin_width = bin_desc["width"]
        #                 keys.append(str(int(row[i + startindex])))
        #             else:
        #                 keys.append(str(row[startindex + i]).strip())
        #
        #         key = ",".join(keys)
        #         print(keys)
        #         print(row)
        #         print('******')
        #         row = list(row)
        #         for i, r in enumerate(row):
        #             if isinstance(r, decimal.Decimal):
        #                 row[i] = float(r)
        #
        #         results[key] = row[len(viz_request.viz.binning) + startindex:]
        #
        #         #if self.can_execute_online(sql_statement) and startindex == 3:
        #         #    margins[key] = row[len(row) - 1:]
        #
        #     viz_request.result = results
        #     viz_request.margins = margins
        #     out_q.put(viz_request)
        #     print("delivering...")
