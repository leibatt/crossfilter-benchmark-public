import json
from common import util

class VizRequest:

    def __init__(self, operation_id, parent_operation_id, expected_start_time, viz, dropped = False):
        self.operation_id = operation_id
        self.parent_operation_id = parent_operation_id
        self.viz = viz
        self.expected_start_time = expected_start_time
        self.start_time = -1
        self.end_time = -1
        self.result = None
        self.margins = None
        self.delivered = False
        self.bins = None
        self.timedout = False
        self.dropped = dropped
       
        self.t_start = 0
        self.t_pause = 0
        self.progress = 0
        self.connection_time=0
            
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)        
