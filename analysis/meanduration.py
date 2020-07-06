import sys
import os
import json
import pandas as pd
import numpy as np, scipy.stats as st

def computeCi95Lower(s):
  return st.t.interval(0.95, len(s) -1, loc=np.mean(s), scale=st.sem(s))[0]

def computeCi95Upper(s):
  return st.t.interval(0.95, len(s) -1, loc=np.mean(s), scale=st.sem(s))[1]

def generate_results_all_dataset_sizes(filepath):
  res = []
  for size in ["size_1M","size_10M","size_100M"]:
    sizeName = size.replace("size_","")
    print("evaluating dataset size",size)
    sizePath = os.path.join(filepath,size)
    if os.path.exists(sizePath):
      res1 = consolidate_results_all_datasets(sizePath)
      for r in res1:
        r["dataset_size"] = sizeName
      res.extend(res1)
  # concatenate everything
  resDf = pd.concat(res)
  #print(resDf.groupby(["dataset_size","dataset","driver"]).count())
  totalQueries = {
    "flights": 368690,
    "movies": 289450,
    "weather": 542976
  }

  aggRes = resDf.groupby(["dataset_size","dataset", "driver"]).agg(
    meanDuration=('duration', 'mean'),
    countAnswered=('duration', 'count'),
    durationCiLower=('duration', computeCi95Lower),
    durationCiUpper=('duration', computeCi95Upper),
    durationStd=('duration', 'std'),
    countViolated=('time_violated', 'sum')
  ).reset_index().copy()
  aggResDescribe = resDf.groupby(["dataset_size","dataset", "driver"]).agg('describe')['duration'].reset_index()
  print(aggResDescribe.to_json(orient="records"))
  aggRes["responseRate"] = aggRes["countAnswered"] - aggRes["countViolated"]
  for i in range(len(aggRes["dataset"])):
    aggRes.loc[i,"responseRate"] = aggRes.loc[i,"responseRate"] * 1.0 / totalQueries[aggRes.loc[i,"dataset"]]
    #print(aggRes.loc[i,"responseRate"])
  return resDf,aggRes

def consolidate_results_all_datasets(filepath):
  res = []
  #for dataset in ["flights","movies"]:
  for dataset in ["flights","movies","weather"]:
    print("\tevaluating dataset",dataset)
    datasetPath = os.path.join(filepath,dataset)
    res1 = consolidate_results_all_drivers(datasetPath)
    res.extend(res1)
  return res

def consolidate_results_all_drivers(filepath):
  res = []
  #for driver in ["duckdb","monetdb","sqlite","postgresql","verdictdb-10","verdictdb-50"]:
  for driver in ["duckdb","monetdb","sqlite","postgresql","verdictdb-10"]:
    print("\t\tevaluating driver",driver)
    driverPath = os.path.join(filepath,driver)
    if os.path.exists(driverPath):
      li = consolidate_results(driverPath)
      res.extend(li)
  return res

# for a given dataset size, dataset name, and driver
def consolidate_results(filepath):
  li = []
  total = 0
  for report in os.listdir(filepath):
    if report.endswith(".csv"):
      #print("\t\t\t",os.path.join(filepath,report))
      df = pd.read_csv(os.path.join(filepath,report))[["dataset","driver", "workflow", "dropped", "duration"]]
      if len(df) > 0 and "_0_workflow" in df["workflow"][0]: # ignore warmup tasks
         print("skipping file",report,"for workflow",df["workflow"][0])
         continue
      #print("\t\tall records before filter",df["dropped"].count())
      df["time_violated"] = df["duration"] >= 100
      total += df["dropped"].count()
      df=df[df["dropped"] == False]
      df["duration"] = df["duration"].astype(int)
      li.append(df)
  print("\t\ttotal records observed",total)
  return li

  #with open("result-duration.csv", "w") as f:
  #      df.to_csv(f)

if __name__ == "__main__":
  if len(sys.argv) > 1:
    filepath = sys.argv[1]
    #df=consolidate_results(filepath)
    #df=consolidate_results_all_drivers(filepath)
    df,durationMeans=generate_results_all_dataset_sizes(filepath)
    print("final results:")
    print(durationMeans.to_json(orient="records"))
    with open(os.path.join(filepath,"final_results.json"),"w") as f:
      f.write(json.dumps(durationMeans.to_json(orient="records")))
  else:
    print("usage: python3 meanduration [path to reports]")
    sys.exit(0)
