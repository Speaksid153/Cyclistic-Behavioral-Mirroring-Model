import pandas as pd
from pathlib import Path

DATA_DIR = Path("./data/processed")

def run_integrity_check():
    file_path = DATA_DIR / "fact_trips.csv"
    
    if not file_path.exists():
        print("❌ Error: fact_trips.csv not found.")
        return

    print("Running Data Integrity Check (Casual-Only Analysis Readiness)...")
    
    # FIX: Load 'started_at' instead of 'hour' since 'hour' is an engineered feature
    df = pd.read_csv(file_path, usecols=['start_station_name', 'started_at', 'member_casual'])
    
    # Calculate hour on the fly to match your notebook logic
    df['hour'] = pd.to_datetime(df['started_at']).dt.hour
    casual_df = df[df['member_casual'] == 'casual']

    missing_stations = casual_df['start_station_name'].isna().sum()
    unique_stations = casual_df['start_station_name'].nunique()
    
    print("-" * 50)
    print(f"Total Casual Rides: {len(casual_df):,}")
    print(f"Missing Station Names: {missing_stations:,} ({(missing_stations/len(casual_df))*100:.2f}%)")
    print(f"Unique Stations: {unique_stations}")
    print(f"Time Range Validated: {casual_df['hour'].min()}h to {casual_df['hour'].max()}h")
    
    if missing_stations > (0.25 * len(casual_df)):
         print("⚠️ WARNING: High null count in station names. Clean the source data.")
    else:
         print("✅ SUCCESS: Data integrity verified for behavioral modeling.")

if __name__ == "__main__":
    run_integrity_check()