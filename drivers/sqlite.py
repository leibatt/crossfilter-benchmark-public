import os
import json
import sqlite3
import datetime, time
import itertools
from common import util
import queue
import threading
from threading import Thread
import logging

import sqlite3
import datetime, time
import itertools
from common import util


class IDEBenchDriver:

    def init(self, options, schema, driver_arg):
        self.time_of_latest_request = 0
        self.isRunning = False
        self.requests = queue.LifoQueue()
        self.config = json.load(open(os.path.join(os.path.dirname(__file__),'..','sqlite.config.json')))

    def create_connection(self):
        sqlite_file = self.config['dbFilename']
        conn = sqlite3.connect(sqlite_file)
        return conn

    def sqlitefix(self, sql_statement):
        if not "FLOOR" in sql_statement:
            return sql_statement
        else:
            sql_statement=sql_statement.replace("FLOOR", "ROUND")
            x=sql_statement.find("ROUND")
            y=sql_statement.find(")",x)
            output=sql_statement[:y]+" -0.5 "+sql_statement[y:]
            #print(output,flush=True)
            return output

    def execute_vizrequest(self, viz_request, options, schema, result_queue):

        viz = viz_request.viz
        sql_statement = viz.get_computed_filter_as_sql(schema)
        #calculate connection time

        connection = self.conn
        cursor = connection.cursor()

        viz_request.start_time = util.get_current_ms_time()
        #print(sql_statement,flush=True,end = '')
     
        cursor.execute(self.sqlitefix(sql_statement))
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
        self.requests.put((viz_request, options, schema, result_queue))

    def process(self):
        self.conn = self.create_connection()

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
        
        # close connection when done
        self.conn.close()

    def workflow_start(self):
        self.isRunning = True
        thread = Thread(target = self.process)
        thread.start()

    def workflow_end(self):
        self.isRunning = False
       
