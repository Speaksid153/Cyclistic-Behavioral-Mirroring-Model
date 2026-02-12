import pandas as pd
from pathlib import Path

# --- Paths ---
BASE_DIR = Path(__file__).resolve().parent.parent
MASTER_PATH = BASE_DIR / "Data" / "Processed Datasets" / "cyclistic_master_dataset.csv"
SEGMENT_PATH = BASE_DIR / "Data" / "Processed Datasets" / "station_behavior_segments.csv"
OUTPUT_PATH = BASE_DIR / "Data" / "Processed Datasets" / "casual_anchor_vs_noise_hourly.csv"

print("Building comparison dataset...")

# Check if sources exist
if not MASTER_PATH.exists() or not SEGMENT_PATH.exists():
    print(f"Error: Ensure {MASTER_PATH.name} and {SEGMENT_PATH.name} exist.")
    exit()

# Load and Filter
df = pd.read_csv(MASTER_PATH, usecols=['started_at', 'member_casual', 'start_station_name'])
segments = pd.read_csv(SEGMENT_PATH, usecols=['start_station_name', 'final_status'])

# Standardize and Extract Hour
df['hour'] = pd.to_datetime(df['started_at']).dt.hour
df = df[df['member_casual'].str.lower() == 'casual']

# Merge
merged = df.merge(segments, on="start_station_name", how="inner")
filtered = merged[merged["final_status"].isin(["Confirmed Behavioral Anchor", "Inconsistent / Noise"])]

# Aggregate
hourly_dist = filtered.groupby(["final_status", "hour"]).size().reset_index(name="rides")
hourly_dist["percentage"] = hourly_dist.groupby("final_status")["rides"].transform(lambda x: (x / x.sum()) * 100)

# SAVE THE FILE
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
hourly_dist.to_csv(OUTPUT_PATH, index=False)

print(f"Success! File created at: {OUTPUT_PATH}")