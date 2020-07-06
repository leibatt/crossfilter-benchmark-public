import json
import csv
import glob
import numpy as np
import os
import statistics
import logging
import ntpath
from scipy import spatial

logger = logging.getLogger("idebench")

class Evaluator: 

    def __init__(self, options):
        self.options = options

    def evaluate(self, workflow_path):
        self.file_name = workflow_path
        logger.info("starting evaluation")
        result_json = None
        try:
            with open(workflow_path, "r") as json_data:
                result_json = json.load(json_data)
        except:
            print("couldn't load file %s" % (workflow_path))
            return

        args = result_json["args"]
        groundtruth = None

        gt_folder_path = os.path.join(self.options.gt_folder, args["driver_name"], args["settings_dataset"], args["settings_size"])
        gt_path = os.path.join(gt_folder_path, args["settings_workflow"] + ".json")

        if gt_path:
            with open(gt_path, "r") as json_data:
                groundtruth = json.load(json_data)["results"]
        
        with open("reports/%s.csv" % os.path.splitext(ntpath.basename(workflow_path))[0], 'w') as fp:
            w = csv.DictWriter(fp, [
                                    "db_query_id",
                                    "file_name",
                                    "event_id",
                                    "dataset",
                                    "dataset_size",
                                    "driver",
                                    "viz_name",
                                    "workflow",
                                    "expected_start_time",
                                    "actual_start_time",
                                    "actual_end_time",
                                    "duration",
                                    "dropped",
                                    "think_time",
                                    "time_requirement",
                                    "time_violated",
                                    "num_binning_dimensions",
                                    "binning_type",                                    
                                    "num_invalid_bins",
                                    "num_bins_out_of_margin",
                                    "num_bins_delivered",
                                    "num_bins_in_gt",
                                    "missing_bins",
                                    "dissimilarity",
                                    "num_aggregates_per_bin",                                    
                                    "aggregate_type",
                                    "bias",
                                    "rel_error_avg",
                                    "rel_error_stdev",
                                    "rel_error_min",
                                    "rel_error_max",
                                    "margin_avg",
                                    "margin_stdev",
                                    "margin_min",
                                    "margin_max",
                                    "margin_ratio",
                                    "progress",], delimiter=",", lineterminator="\n")
            w.writeheader()

            operations = result_json["results"]
            operation_counter = 0
            for op_id in operations.keys():
                
                rel_error    = 0
                margins      = []
                invalid_bins = []
                missing_bins = 0
                out_of_margin_count = 0

                if groundtruth and op_id in groundtruth and groundtruth[op_id]["output"]:
                    gt_output = groundtruth[op_id]["output"]
                    op_output = operations[op_id]["output"]

                    rel_error = self.compute_mean_relative_error(op_output, gt_output)
                    missing_bins = self.compute_missing_bins(op_output, gt_output)
                    invalid_bins = self.compute_invalid_bins(op_output, gt_output)
                    operation_counter += 1

                operation = operations[op_id]
                
                op_eval_result = {}
                op_eval_result["db_query_id"] = operation["id"]
                op_eval_result["file_name"] = self.file_name
                op_eval_result["event_id"] = operation["event_id"]
                op_eval_result["dataset"] = args["settings_dataset"]
                op_eval_result["dataset_size"] = args["settings_size"]
                op_eval_result["viz_name"] = operation["viz_name"]
                op_eval_result["think_time"] = args["settings_thinktime"]
                op_eval_result["time_requirement"] = args["settings_time_requirement"]
                op_eval_result["driver"] = args["driver_name"]
                op_eval_result["workflow"] = args["settings_workflow"]
                op_eval_result["expected_start_time"] = operation["expected_start_time"]
                op_eval_result["actual_start_time"] = operation["start_time"]
                op_eval_result["actual_end_time"] = operation["end_time"]
                op_eval_result["duration"] = operation["end_time"] - operation["start_time"]
                op_eval_result["dropped"] = operation["dropped"]
            
                if "time_violated" in operation:
                    op_eval_result["time_violated"] = operation["time_violated"]
                elif "timedout" in operation:
                    op_eval_result["time_violated"] = operation["timedout"]
                else:
                    raise Exception()

                op_eval_result["num_invalid_bins"] = len(invalid_bins)
                op_eval_result["binning_type"] = operation["binning_type"]
                op_eval_result["aggregate_type"] = operation["aggregate_type"]
                op_eval_result["num_bins_in_gt"] = 0
                op_eval_result["missing_bins"] = "%.5f" %  missing_bins if missing_bins else 0
                op_eval_result["dissimilarity"] = 0
                op_eval_result["num_bins_out_of_margin"] = "%i" % out_of_margin_count
                op_eval_result["num_aggregates_per_bin"] = operation["num_aggregates_per_bin"]       
                op_eval_result["num_binning_dimensions"] = operation["num_binning_dimensions"]     
                op_eval_result["progress"] = "%.5f" %  operation["progress"]
                op_eval_result["bias"] = 0
                #op_eval_result["rel_error_stdev"] = 0
                #op_eval_result["rel_error_min"] = 0
                #op_eval_result["rel_error_max"] = 0
                op_eval_result["rel_error_avg"] = "%.5f" % float(rel_error)
                op_eval_result["margin_stdev"] = "%.5f" % statistics.stdev(margins) if len(margins) > 1 else 0.0
                op_eval_result["margin_min"] = "%.5f" % min(margins) if len(margins) > 0 else 0.0
                op_eval_result["margin_max"] = "%.5f" % max(margins) if len(margins) > 0 else 0.0
                op_eval_result["margin_avg"] = "%.5f" % float(sum(margins) / float(len(margins))) if len(margins) > 0 else 0.0
                op_eval_result["margin_ratio"] = "%.5f" % float(len(operation["margins"]) / len(operation["output"])) if operation["margins"] and len(operation["output"]) > 0 else  1
                w.writerow(op_eval_result)

        logger.info("evalation done")
        logger.info(operation_counter)

    def compute_missing_bins(self, op_output, gt_output):
        return 1 - len(op_output.keys()) / len(gt_output.keys()) if len(gt_output.keys()) > 0 else 0

    def compute_mean_relative_error(self, op_output, gt_output):
        gt_values = []
        diff_sum = 0
        for gt_bin_identifier, gt_aggregate_results in gt_output.items():
            if gt_bin_identifier in op_output:                        
                op_bin_value = op_output[gt_bin_identifier]
                gt_bin_value = gt_aggregate_results[0]
                delta = op_bin_value - gt_bin_value
                diff_sum += (delta * delta)
                gt_values.append(gt_bin_value)            
            else:
                pass # ignore missing bins for mean relative error
        return np.sqrt(diff_sum) / (np.linalg.norm(np.array(gt_values)))


    def compute_invalid_bins(self, op_output, gt_output):
        invalid_bins = []
        for operation_id in op_output.keys():
            if operation_id not in gt_output:
                invalid_bins.append(operation_id)
        return invalid_bins

