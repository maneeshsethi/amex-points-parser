import pandas as pd
import os
import sys
from glob import glob
from datetime import datetime

# Get the directory path from command-line arguments
if len(sys.argv) < 2:
    print("Usage: python script.py /path/to/your/csvs")
    sys.exit(1)

directory_path = sys.argv[1]

# Load and merge all CSV files
all_files = glob(os.path.join(directory_path, "*.csv"))
df_list = [pd.read_csv(file) for file in all_files]
df = pd.concat(df_list, ignore_index=True)

# Clean Amount column (remove '$', convert to float)
df['Amount'] = df['Amount'].replace(r'[\$,]', '', regex=True).astype(float)

# Ensure Points/Miles is numeric
df['Points/Miles'] = pd.to_numeric(df['Points/Miles'], errors='coerce')

# Identify 4.0x rows
df['Is4x'] = df['Multiplier'].str.strip() == '4.0x'

# Sort accordingly
df_sorted = df.sort_values(by=['Is4x', 'Date'], ascending=[False, True])

# Group by Card and Is4x, then aggregate
grouped = df_sorted.groupby(['Card', 'Is4x']).agg({
    'Amount': 'sum',
    'Points/Miles': 'sum'
}).reset_index()

# Rename columns for clarity
grouped['Category'] = grouped['Is4x'].map({True: '4.0x', False: 'Other'})
grouped = grouped[['Card', 'Category', 'Amount', 'Points/Miles']]

# Format Amount as US currency and Points/Miles as integer with commas
grouped['Amount'] = grouped['Amount'].apply(lambda x: f"${x:,.2f}")
grouped['Points/Miles'] = grouped['Points/Miles'].apply(lambda x: f"{int(x):,}")

# Output the grouped summary
print(grouped)

# Export to CSV with ISO datetime filename
iso_time = datetime.now().isoformat(timespec='seconds').replace(":", "-")
export_filename = f"export_results_{iso_time}.csv"
export_path = os.path.join(directory_path, export_filename)
grouped.to_csv(export_path, index=False)
print(f"Results exported to: {export_path}")
