import pandas as pd
from pathlib import Path
import sys

# -------------------------------
# 1. PATH SETUP 
# -------------------------------
# This script is in: DIVVY PROJECT/Scripts/Extra Validation/
SCRIPT_DIR = Path(__file__).resolve().parent


PROJECT_ROOT = SCRIPT_DIR.parent.parent 

file_path = PROJECT_ROOT / 'Data' / 'Processed Datasets' / 'cyclistic_casual_only.csv'

# -------------------------------
# 2. LOAD DATA
# -------------------------------
print(f"Searching for file at: {file_path}")

if not file_path.exists():
    print("ERROR: File not found!")
    print(f"Current Root: {PROJECT_ROOT}")
    print("Check if your Data folder is in the root and not inside Scripts.")
    sys.exit(1)

print("Loading casual-only dataset...")
# Using usecols to save memory
df = pd.read_csv(file_path, usecols=['ride_id', 'start_station_name', 'hour', 'day_of_week', 'month'])
print(f"Dataset loaded. Total rows: {len(df):,}\n")

# -------------------------------
# 3. VALIDATION LOGIC
# -------------------------------
print("--- Dataset Info & Missing Values ---")
print(df.info())
print("\nMissing values per column:")
print(df.isna().sum())

print("\n--- Unique Values & Ranges ---")
print("Unique values in 'day_of_week':", df['day_of_week'].unique())
print("Hour range:", df['hour'].min(), "to", df['hour'].max())
print("Number of unique start stations:", df['start_station_name'].nunique())
print("Months present in data:", df['month'].unique())

print("\n--- Quick Statistics ---")
print(df['hour'].describe())

print("\n--- Sample Data ---")
print(df.head())