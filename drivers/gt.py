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
        pass

    def create_connection(self):
        conn = pymonetdb.connect(username="crossfilter", password="XA*yiTx_8Hko", hostname="localhost", port=50000, database="crossfilter-eval-db")
        return conn

    def execute_vizrequest(self, viz_request, options, schema, result_queue):

        viz = viz_request.viz
        sql_statement = viz.get_computed_filter_as_sql(schema)
        cursor = self.conn.cursor()

        viz_request.start_time = util.get_current_ms_time()
        cursor.execute(sql_statement)
        data = cursor.fetchall()
        viz_request.end_time = util.get_current_ms_time()

        cursor.close()

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
        self.execute_vizrequest(viz_request, options, schema, result_queue)

    def workflow_start(self):
        self.conn = self.create_connection()

    def workflow_end(self):
        self.conn.close()