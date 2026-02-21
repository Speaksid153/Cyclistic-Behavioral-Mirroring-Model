import pandas as pd
import numpy as np
from pathlib import Path

# Config
DATA_DIR = Path("./data/processed")

def haversine_distance(lat1, lon1, lat2, lon2):
    """Vectorized Haversine formula to calculate distance in KM."""
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
    return 2 * np.arcsin(np.sqrt(a)) * 6371

def run_geospatial_analysis():
    input_path = DATA_DIR / "fact_trips.csv"
    if not input_path.exists():
        print("❌ Error: fact_trips.csv not found. Run pipeline.py first.")
        return

    # Loading coordinates and ride_id
    try:
        df = pd.read_csv(input_path, usecols=['ride_id', 'start_lat', 'start_lng', 'end_lat', 'end_lng', 'ride_length', 'member_casual'])
    except ValueError:
        print("❌ Error: Coordinates missing in fact_trips.csv. Ensure pipeline.py includes them.")
        return

    print(f"Calculating distances for {len(df):,} rides...")

    # Calculate straight-line distance
    df['dist_km'] = haversine_distance(
        df['start_lat'], df['start_lng'], 
        df['end_lat'].fillna(df['start_lat']), df['end_lng'].fillna(df['start_lng'])
    )

    # Logic: Flag "Leisure Loops" (Started/Ended at same place, but rode for > 10 mins)
    df['is_leisure_loop'] = (df['ride_length'] > 10) & (df['dist_km'] < 0.3)

    output_path = DATA_DIR / "geospatial_metrics.csv"
    df[['ride_id', 'dist_km', 'is_leisure_loop']].to_csv(output_path, index=False)
    
    print("-" * 40)
    print(f"✅ SUCCESS: Geospatial metrics saved to {output_path}")
    print(f"Leisure Loops identified: {df['is_leisure_loop'].sum():,}")

if __name__ == "__main__":
    run_geospatial_analysis()