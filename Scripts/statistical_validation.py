import pandas as pd
from pathlib import Path

# --- Setup Paths ---
DATA_DIR = Path("./data/processed")

def run_statistical_validation():
    master_path = DATA_DIR / "fact_trips.csv"
    segment_path = DATA_DIR / "station_behavior_segments.csv"
    output_path = DATA_DIR / "hourly_validation_metrics.csv"

    if not master_path.exists() or not segment_path.exists():
        print("❌ Error: Required datasets missing. Run pipeline and segmentation first.")
        return

    print("Building Hourly Statistical Validation dataset...")

    # 1. Load data - only pulling casuals
    df = pd.read_csv(master_path, usecols=['started_at', 'member_casual', 'start_station_name'])
    df = df[df['member_casual'] == 'casual'].copy()
    
    segments = pd.read_csv(segment_path, usecols=['start_station_name', 'final_status'])

    # 2. Extract Hour and Merge
    df['hour'] = pd.to_datetime(df['started_at']).dt.hour
    merged = df.merge(segments, on="start_station_name", how="inner")

    # 3. Filter for comparison (Anchors vs. Noise)
    filtered = merged[merged["final_status"].isin(["Confirmed Behavioral Anchor", "Inconsistent / Noise"])]

    # 4. Aggregate Hourly Distribution
    hourly_dist = filtered.groupby(["final_status", "hour"]).size().reset_index(name="rides")
    
    # Calculate % share of the day per group
    hourly_dist["pct_of_daily_rides"] = (
        hourly_dist.groupby("final_status")["rides"]
        .transform(lambda x: (x / x.sum()) * 100)
    )

    # 5. Save Output
    hourly_dist.to_csv(output_path, index=False)
    
    print("-" * 50)
    print(f"✅ SUCCESS: Validation metrics saved to {output_path}")
    print("This file will power your 'Behavioral Peak' Line Chart in Power BI.")

if __name__ == "__main__":
    run_statistical_validation()