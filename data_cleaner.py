import pandas as pd
import re

file_name = ["iitmain.csv", "csab.csv"]

def extract_integer(value):
    match = re.search(r'\d+', str(value))
    return int(match.group()) if match else value

for file in file_name:
    df = pd.read_csv(file, header=None)
    df[5] = df[5].apply(extract_integer)
    df[6] = df[6].apply(extract_integer)
    df.to_csv(file, index=False, header=False)

print("Processing complete!")