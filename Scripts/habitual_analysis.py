import pandas as pd
import numpy as np
from pathlib import Path

# Config
DATA_DIR = Path("./data/processed")
RUSH_WINDOW = [7, 8, 9, 17, 18, 19]

def run_habitual_analysis():
    input_path = DATA_DIR / "fact_trips.csv"
    if not input_path.exists():
        print("❌ Error: fact_trips.csv not found. Run pipeline.py first.")
        return

    # Load only what we need. 'is_commute' was already calculated in our pipeline.
    df = pd.read_csv(input_path, usecols=['start_station_name', 'started_at', 'member_casual', 'is_commute'])
    
    # Filter for Casuals and fix types
    df = df[df['member_casual'] == 'casual'].copy()
    df['started_at'] = pd.to_datetime(df['started_at'])
    df['month'] = df['started_at'].dt.month_name()
    df['hour'] = df['started_at'].dt.hour
    df['day_name'] = df['started_at'].dt.day_name()

    print(f"Analyzing habitual patterns for {len(df):,} casual rides...")

    # 1. Volume Check: We only care about stations with enough data to be statistically relevant
    station_monthly_vol = df.groupby(['start_station_name', 'month']).size().reset_index(name='vol')
    vol_threshold = station_monthly_vol['vol'].quantile(0.75) # Focus on top 25% active stations
    valid_stations = station_monthly_vol[station_monthly_vol['vol'] >= vol_threshold]
    
    # 2. Hourly Consistency (Ch)
    df['in_rush'] = df['hour'].isin(RUSH_WINDOW).astype(int)
    ch_scores = df.groupby(['start_station_name', 'month'])['in_rush'].mean().reset_index(name='Ch')

    # 3. Mid-week Focus (Cd)
    midweek_days = ['Tuesday', 'Wednesday', 'Thursday']
    df['is_midweek'] = df['day_name'].isin(midweek_days).astype(int)
    cd_scores = df.groupby(['start_station_name', 'month'])['is_midweek'].mean().reset_index(name='Cd')

    # 4. Final Scoring Logic: 60% Rush Hour + 40% Midweek
    results = valid_stations.merge(ch_scores, on=['start_station_name', 'month'])
    results = results.merge(cd_scores, on=['start_station_name', 'month'])
    results['routine_score'] = (results['Ch'] * 0.6) + (results['Cd'] * 0.4)
    
    # Tiering for Power BI filters
    results['tier'] = pd.cut(
        results['routine_score'], 
        bins=[0, 0.25, 0.45, 1.0], 
        labels=['Low', 'Emerging', 'Strong']
    )

    output_path = DATA_DIR / "habitual_metrics.csv"
    results.sort_values('routine_score', ascending=False).to_csv(output_path, index=False)
    print(f"✅ SUCCESS: Habitual metrics saved to {output_path}")

if __name__ == "__main__":
    run_habitual_analysis()