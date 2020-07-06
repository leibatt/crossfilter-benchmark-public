import pandas as pd
import os


datasets = ["movies", "weather"]

li = []
for dataset in datasets:
    folder = "data/" + dataset + "/"
    for filename in os.listdir(folder):
        filename = folder + filename
        if ".csv" in filename:
                df = pd.read_csv(filename)[["driver", "workflow", "dropped", "duration", "event_id"]]
                li.append(df)
df = pd.concat(li, axis=0, ignore_index=True)



#df = df[ (df["duration"] > 5) & (df["duration"] < 100) ]
df = df.groupby([ "driver",  "dropped"]).count().reset_index()

print(df)

with open("result-x.csv", "w") as f:
        df.to_csv(f)



#df_dropped = df[df["dropped"] == True]
#df_dropped = df_dropped.groupby([ "driver",  "workflow"])["dropped"].count().reset_index()
#print(df_dropped)

#df_nondropped = df[df["dropped"] == False]
#df_nondropped.rename(columns={"dropped": "nondropped"}, inplace=True)
#df_nondropped = df_nondropped.groupby([ "driver",  "workflow"])["nondropped"].count().reset_index()

#df = df_dropped.join(df_nondropped, on=["driver", "workflow"])
