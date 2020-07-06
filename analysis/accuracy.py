import sys
import os
import glob
import pandas as pd

def get_consolidate_report():
    all_dfs = []
    for report_path in glob.glob(os.path.join(sys.argv[1], "**/*.csv"), recursive=True):
        df = pd.read_csv(report_path)
        df = df[ (df["dropped"] == False) & (df["duration"] < 100)]
        all_dfs.append(df)
    return pd.concat(all_dfs)

def evaluate_accuracy(df):
    df["rel_error_avg"] /= df.shape[0]
    return df.groupby(["driver", "dataset_size"]).agg(meanRelError=("rel_error_avg", "sum"), meanRelErrorStd=("rel_error_avg", "std"),eanRelErrorMax=("rel_error_avg", "max"),missingBins=("missing_bins", "mean"), missingBinsStd=("missing_bins", "std"))

def num_missing_bins(df):
    return df.groupby(["driver", "dataset_size"]).agg(numRecords=("missing_bins", "mean"))


if __name__ == "__main__":
    if len(sys.argv) == 2:
        df = get_consolidate_report()
        print(df.shape)
        result = evaluate_accuracy(df).reset_index()
        print(result)
    else:
        print("usage: python3 generate-verdictdb-gt.py [path to reports folder]")
        sys.exit(1)
