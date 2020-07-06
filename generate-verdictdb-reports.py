import sys
import glob
import os
import json
import subprocess
import time

if __name__ == "__main__":
    if len(sys.argv) == 3:
        for workflow_path in glob.glob(os.path.join(sys.argv[1], "**/*.json"), recursive=True):
            with open(workflow_path, "r") as f:
                workflow = json.load(f)
                args = workflow["args"]
                os.system("python3 idebench.py --evaluate %s --gt-folder %s" % (workflow_path, sys.argv[2]))
    else:
        print("usage: python3 formatWeather.py [workflow filepath] [groundtruth folder]")
        sys.exit(1)
