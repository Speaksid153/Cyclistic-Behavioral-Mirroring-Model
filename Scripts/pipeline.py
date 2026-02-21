import pandas as pd
import numpy as np
from pathlib import Path

# =========================
# CONFIGURATION
# =========================
RAW_DIR = Path("./data/raw")
PROCESSED_DIR = Path("./data/processed")
MIN_TRIPS_FOR_STABILITY = 50 

def run_analytics_pipeline():
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    
    all_files = list(RAW_DIR.glob("*.csv"))
    if not all_files:
        raise FileNotFoundError(f"No CSVs found in {RAW_DIR}.")

    # DATA CONTRACT: We must keep lats/lngs for the Geospatial script
    keep_cols = [
        'ride_id', 'started_at', 'ended_at', 'member_casual',
        'start_station_name', 'start_lat', 'start_lng', 'end_lat', 'end_lng'
    ]
    
    print(f"Processing {len(all_files)} files...")
    df = pd.concat((pd.read_csv(f, usecols=lambda x: x.lower() in keep_cols) for f in all_files), ignore_index=True)
    df.columns = df.columns.str.lower()

    # Cleaning
    df['started_at'] = pd.to_datetime(df['started_at'], errors='coerce')
    df['ended_at'] = pd.to_datetime(df['ended_at'], errors='coerce')
    df = df.dropna(subset=['started_at', 'start_station_name'])
    
    df['ride_length'] = (df['ended_at'] - df['started_at']).dt.total_seconds() / 60
    df = df[(df['ride_length'] > 1) & (df['ride_length'] < 1440)]

    # Feature Engineering
    df['hour'] = df['started_at'].dt.hour
    df['is_weekday'] = df['started_at'].dt.dayofweek < 5
    is_rush = df['hour'].isin([7, 8, 9, 10, 16, 17, 18, 19])
    df['is_commute'] = is_rush & df['is_weekday'] & (df['ride_length'] <= 30)

    # 1. Export DIM_STATIONS
    station_dim = df.groupby('start_station_name').agg({
        'start_lat': 'mean',
        'start_lng': 'mean'
    }).reset_index()
    station_dim.to_csv(PROCESSED_DIR / "dim_stations.csv", index=False)

    # 2. Export FACT_TRIPS (Now including coordinates for downstream analysis)
    fact_cols = [
        'ride_id', 'start_station_name', 'started_at', 'member_casual', 
        'is_commute', 'ride_length', 'start_lat', 'start_lng', 'end_lat', 'end_lng'
    ]
    df[fact_cols].to_csv(PROCESSED_DIR / "fact_trips.csv", index=False)

    print(f"✅ SUCCESS: Pipeline re-run complete. Fact table now contains coordinates.")

if __name__ == "__main__":
    run_analytics_pipeline()