import pandas as pd
from pathlib import Path

# --- Setup Paths ---
DATA_DIR = Path("./data/processed")

def run_mirror_correlation():
    # File paths
    master_path = DATA_DIR / "fact_trips.csv"
    anchor_path = DATA_DIR / "station_behavior_segments.csv"
    output_path = DATA_DIR / "mirror_correlation_results.csv"
    
    # Check if files exist
    if not master_path.exists() or not anchor_path.exists():
        print(f"❌ Error: Required files missing in {DATA_DIR}")
        return

    print("Starting Behavioral Mirroring Analysis...")
    
    # --- THE FIX ---
    # We load 'started_at' and create the 'hour' feature on the fly.
    # The 'hour' column does not exist in your raw fact_trips.csv.
    df = pd.read_csv(master_path, usecols=['start_station_name', 'started_at', 'member_casual'])
    
    print("Converting timestamps and deriving hour...")
    df['started_at'] = pd.to_datetime(df['started_at'])
    df['hour'] = df['started_at'].dt.hour
    
    # Load elite anchor names from your segmentation results
    anchors = pd.read_csv(anchor_path)
    elite_anchors = anchors[anchors['final_status'] == 'Confirmed Behavioral Anchor']['start_station_name'].tolist()
    
    if not elite_anchors:
        print("⚠️ No 'Confirmed Behavioral Anchors' found. Check your segmentation thresholds.")
        return

    results = []
    for station in elite_anchors:
        subset = df[df['start_station_name'] == station]
        
        # Calculate hourly distributions (normalized)
        casual_dist = subset[subset['member_casual'] == 'casual']['hour'].value_counts(normalize=True).sort_index()
        member_dist = subset[subset['member_casual'] == 'member']['hour'].value_counts(normalize=True).sort_index()
        
        # Align index to ensure 0-23 hours are compared correctly
        full_index = pd.Index(range(24))
        casual_dist = casual_dist.reindex(full_index, fill_value=0)
        member_dist = member_dist.reindex(full_index, fill_value=0)
        
        # Pearson Correlation (0.0 to 1.0)
        correlation = casual_dist.corr(member_dist)
        
        results.append({
            "Station": station,
            "Mirror_Correlation": round(correlation, 4),
            "Verdict": "Strong Mirror" if correlation >= 0.85 else "Weak Alignment"
        })

    # Save and Print Results
    mirror_df = pd.DataFrame(results).sort_values(by="Mirror_Correlation", ascending=False)
    mirror_df.to_csv(output_path, index=False)
    
    print("-" * 50)
    print("ELITE ANCHOR CORRELATION RESULTS:")
    print(mirror_df.to_string(index=False))
    print(f"\n✅ SUCCESS: Mirror analysis saved to {output_path}")

if __name__ == "__main__":
    run_mirror_correlation()