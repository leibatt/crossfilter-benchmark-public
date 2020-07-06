import os
import json

useFixed = {"flights":False,"movies":True,"weather":False}
workflowPaths = {
  "flights":"../data/flights/workflows/",
  "weather":"../data/weather/workflows/",
  "movies":"../data/movies/workflows/"
}
res = []
dres = []
for dataset in ["flights","weather","movies"]:
  d = workflowPaths[dataset]
  totalCount = 0
  totalViews = None
  for report in os.listdir(d):
    if (not useFixed[dataset] and report.endswith("workflow.json")) or (useFixed[dataset] and report.endswith("fixed.json")):
      with open(os.path.join(d,report)) as f:
        r = json.load(f)
        totalViews = len(r["setup"])
        totalInteractions = len(r["interactions"])
        res.append({"dataset":"flights","workflow_name":report,"totalInteractions":totalInteractions,"totalViews":totalViews,"totalQueries":totalInteractions*(totalViews-1)})
        totalCount += totalInteractions
  dres.append({"dataset":dataset,"totalInteractions":totalCount,"totalViews":totalViews,"totalQueries":totalCount*(totalViews-1)})
  print(dataset,totalCount,totalViews,totalCount*(totalViews-1))

print(json.dumps(res))
print("\n")
print(json.dumps(dres))
