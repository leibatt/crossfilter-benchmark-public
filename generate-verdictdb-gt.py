import sys
import glob
import os
import json
import subprocess
import time


if __name__ == "__main__":
    if len(sys.argv) == 3:
        # recursively finds all workflow results in the given folder and computes the groundtruth for them
        for workflow_path in glob.glob(os.path.join(sys.argv[1], "**/*.json"), recursive=True):
            with open(workflow_path, "r") as f:
                workflow = json.load(f)
                args = workflow["args"]
                os.system("python3 idebench.py --driver-name gt --settings-size %s --settings-dataset %s --gt-for %s --gt-folder %s groundtruth --groundtruth" % (args["settings_size"], args["settings_dataset"], workflow_path, str(sys.argv[2])))
    else:
        print("usage: python3 generate-verdictdb-gt.py [path to result folder] [new groundtruth folder]")
        sys.exit(1)