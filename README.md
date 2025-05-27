# AMEX CSV Analyzer

This Python script processes and summarizes CSV transaction files exported from American Express. It aggregates spending and reward points data by card and multiplier category, then outputs a clean, formatted summary both to the console and a timestamped CSV file.

## Features

- Merges all CSVs in a specified directory.
- Cleans and standardizes monetary and points/miles values.
- Identifies and separates `4.0x` multiplier transactions from others.
- Groups totals by individual card number and multiplier category.
- Outputs formatted results (currency, commas) to console.
- Saves the summary as `export_results_<ISO_DATETIME>.csv`.

## Requirements

- Python 3.6+
- `pandas`

Install dependencies:

```bash
pip install pandas
