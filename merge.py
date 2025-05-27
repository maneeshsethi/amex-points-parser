import os
import sys
import pandas as pd
from glob import glob

# Get the directory path from command-line arguments
if len(sys.argv) < 2:
    print("Usage: python merge_csvs.py /path/to/csvs")
    sys.exit(1)

directory_path = sys.argv[1]

# Get all CSV files in the directory
csv_files = glob(os.path.join(directory_path, "*.csv"))

# Return if no files found
if not csv_files:
    print("No CSV files found in the directory.")
    sys.exit(1)

# Read the first file with header
df_main = pd.read_csv(csv_files[0])

# Read remaining files without headers and append to the main DataFrame
for file in csv_files[1:]:
    df = pd.read_csv(file, header=0)
    if df.columns.equals(df_main.columns):
        df_main = pd.concat([df_main, df], ignore_index=True)
    else:
        df = pd.read_csv(file, header=None, skiprows=1)
        df.columns = df_main.columns
        df_main = pd.concat([df_main, df], ignore_index=True)

# Output the merged DataFrame
output_file = os.path.join(directory_path, "merged_output.csv")
df_main.to_csv(output_file, index=False)
print(f"Merged CSV saved to: {output_file}")
