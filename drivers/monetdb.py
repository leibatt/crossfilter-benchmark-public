import pymonetdb
import datetime, time
import itertools
import csv
import json
import os
import queue
import multiprocessing
import threading
from threading import Thread
import logging
from subprocess import call
from common import util

logger = logging.getLogger("idebench")
class IDEBenchDriver:

    def init(self, options, schema, driver_arg):
        self.time_of_latest_request = 0
        self.isRunning = False
        self.requests = queue.LifoQueue()
        self.config = json.load(open(os.path.join(os.path.dirname(__file__),'..','monetdb.config.json')))

    def create_connection(self):
        #conn = pymonetdb.connect(username="monetdb", password="monetdb", hostname="localhost", port=50000, database="crossfilter")
        conn = pymonetdb.connect(username="crossfilter", password=self.config['password'], hostname=self.config["host"], port=self.config['port'], database="crossfilter-eval-db")
        return conn

    def execute_vizrequest(self, viz_request, options, schema, result_queue):

        viz = viz_request.viz
        sql_statement = viz.get_computed_filter_as_sql(schema)
        #calculate connection time

        # get a connection from the pool - block if non is available
        connection = self.pool.get()
        cursor = connection.cursor()

        viz_request.start_time = util.get_current_ms_time()
        cursor.execute(sql_statement)
        data = cursor.fetchall()
        viz_request.end_time = util.get_current_ms_time()


        # put connection back in the queue so the next thread can use it.
        cursor.close()
        self.pool.put(connection)

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
            except:
                # ignore queue-empty exceptions
                pass


    def workflow_start(self):
         # pool a number of db connections
        self.isRunning = True
        self.pool = queue.Queue()
        for i in range(10):
            conn = self.create_connection()
            self.pool.put(conn)

        thread = Thread(target = self.process)
        thread.start()

    def workflow_end(self):
        self.isRunning = False
        # close all db connections at the end of a workflow
        for i in range(self.pool.qsize()):
            conn = self.pool.get(timeout=1)
            conn.close()
