import pandas as pd
from pathlib import Path

# =========================
# 1. PATH SETUP 
# =========================
# This script is in 'DIVVY PROJECT/Scripts/'
SCRIPT_DIR = Path(__file__).resolve().parent

# Move up one level to 'DIVVY PROJECT/'
PROJECT_ROOT = SCRIPT_DIR.parent 

# Define paths relative to the project root
input_folder = PROJECT_ROOT / 'Data' / 'Raw Datasets'
output_folder = PROJECT_ROOT / 'Data' / 'Processed Datasets'

# Automatic folder creation (No more manual setup)
output_folder.mkdir(parents=True, exist_ok=True)

# =========================
# 2. LOAD & MERGE CSV FILES
# =========================
# This finds all CSVs in the raw folder
all_files = list(input_folder.glob("*.csv"))

if not all_files:
    print(f"❌ ERROR: No CSV files found in: {input_folder}")
    print("Ensure your CSV files are inside the 'Data/Raw Datasets' folder.")
    exit()

print(f"Found {len(all_files)} CSV files. Merging now (this may take a moment)...")

# Efficiently load all CSVs
df_list = [pd.read_csv(file) for file in all_files]
df = pd.concat(df_list, ignore_index=True)

# =========================
# 3. NORMALIZE COLUMN NAMES
# =========================
df.columns = df.columns.str.strip().str.lower()

# =========================
# 4. DATETIME CONVERSION
# =========================
print("Converting timestamps...")
df['started_at'] = pd.to_datetime(df['started_at'], errors='coerce')
df['ended_at'] = pd.to_datetime(df['ended_at'], errors='coerce')

# Drop rows with invalid timestamps
df = df.dropna(subset=['started_at', 'ended_at'])

# =========================
# 5. RIDE DURATION
# =========================
df['ride_length'] = (df['ended_at'] - df['started_at']).dt.total_seconds() / 60

# Remove invalid durations (rides that ended before they started)
df = df[df['ride_length'] > 0]

# =========================
# 6. TIME-BASED FEATURES
# =========================
df['hour'] = df['started_at'].dt.hour
df['day_of_week'] = df['started_at'].dt.day_name()
df['month'] = df['started_at'].dt.month_name()
df['month_num'] = df['started_at'].dt.month
df['is_weekend'] = df['day_of_week'].isin(['Saturday', 'Sunday']).astype(int)

# =========================
# 7. RIDE LENGTH BUCKETS
# =========================
df['ride_length_bucket'] = pd.cut(
    df['ride_length'],
    bins=[0, 10, 30, 60, 120, 10000],
    labels=['very_short', 'short', 'medium', 'long', 'very_long']
)

# =========================
# 8. BEHAVIORAL FLAGS
# =========================
# Commute-like rides: Weekdays, during rush hour, under 30 mins
df['commuter_flag'] = (
    (df['hour'].between(7, 10) | df['hour'].between(17, 20)) &
    (df['is_weekend'] == 0) &
    (df['ride_length'] <= 30)
)

# High conversion potential: Casual riders acting like commuters
df['high_conversion_potential'] = (
    (df['member_casual'] == 'casual') &
    (df['commuter_flag'])
)

# =========================
# 9. MASTER DATASET SAVING
# =========================
master_cols = [
    'ride_id', 'rideable_type', 'started_at', 'ended_at',
    'start_station_name', 'start_station_id', 'end_station_name', 'end_station_id',
    'start_lat', 'start_lng', 'end_lat', 'end_lng',
    'member_casual', 'ride_length', 'ride_length_bucket',
    'hour', 'day_of_week', 'month', 'month_num',
    'is_weekend', 'commuter_flag', 'high_conversion_potential'
]

# Ensure only existing columns are exported to avoid errors 
df_master = df.reindex(columns=master_cols)

master_path = output_folder / 'cyclistic_master_dataset.csv'
df_master.to_csv(master_path, index=False)

print("-" * 40)
print(f"SUCCESS: Master dataset saved to: {master_path}")
print(f"Total Rows Processed: {len(df_master):,}")
print("Pipeline finished successfully.")