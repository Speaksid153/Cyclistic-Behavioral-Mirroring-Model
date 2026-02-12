import pandas as pd
from pathlib import Path

# =========================
# 1. PATH SETUP 
# =========================
# This script is in 'DIVVY PROJECT/Scripts/'
SCRIPT_DIR = Path(__file__).resolve().parent

# Move up one level to 'DIVVY PROJECT/' to find the Data folder
PROJECT_ROOT = SCRIPT_DIR.parent 

input_path = PROJECT_ROOT / 'Data' / 'Processed Datasets' / 'cyclistic_master_dataset.csv'
output_path = PROJECT_ROOT / 'Data' / 'Processed Datasets' / 'cyclistic_casual_only.csv'

# =========================
# 2. DATA LOADING & FILTERING
# =========================
print(f"Checking for master dataset at: {input_path}")

if not input_path.exists():
    print(f"❌ ERROR: Cannot find the master dataset.")
    print("Make sure you run the 'Master dataset cleaned.py' script first!")
    exit()

print("Loading master dataset...")
df = pd.read_csv(input_path)
print(f"Total rows in master dataset: {len(df):,}")

# Filter only casual users
# .copy() is important here to avoid 'SettingWithCopy' warnings later
casuals = df[df['member_casual'] == 'casual'].copy()
print(f"Rows after removing members: {len(casuals):,}")

# =========================
# 3. SAVING
# =========================
# Ensure the directory exists (just in case)
output_path.parent.mkdir(parents=True, exist_ok=True)

casuals.to_csv(output_path, index=False)
print("-" * 40)
print(f"SUCCESS: Casual-only dataset saved to: {output_path}")