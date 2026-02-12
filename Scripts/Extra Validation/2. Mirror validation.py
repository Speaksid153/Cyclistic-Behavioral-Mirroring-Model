import pandas as pd
from pathlib import Path

# --- Setup Paths ---
# Reaching back to the master data and the results from script 02
master_data_path = Path('Data/Processed Datasets/cyclistic_master_dataset.csv')
habitual_metrics_path = Path('Data/Processed Datasets/monthly_conversion_metrics.csv')
output_path = Path('Data/Processed Datasets/mirror_validation_results.csv')

# --- Configuration ---
# We're testing the top 20 zones to see if our RS score actually predicts member-like behavior
TOP_N = 20  
MIN_RIDES = 50  # We need at least 50 rides for each group to make the correlation meaningful

print(" Starting Behavioral Validation: Do casuals actually 'mirror' members?")

# --- Load Data ---
try:
    # Pro-tip: Only loading the columns we actually need to save RAM
    cols_to_use = ['start_station_name', 'month', 'hour', 'member_casual']
    df = pd.read_csv(master_data_path, usecols=cols_to_use)
    zones = pd.read_csv(habitual_metrics_path)
    print(f"Datasets loaded. Testing the top {TOP_N} habitual zones...")
except FileNotFoundError as e:
    print(f" Error: Could not find files. {e}")
    exit()

# Cleaning up the master data for analysis
df = df.dropna(subset=['start_station_name'])

# Pulling our 'Elite' targets based on the Routine Score (RS) we calculated earlier
top_targets = zones.sort_values('RS', ascending=False).head(TOP_N)

validation_results = []

# --- The Validation Loop ---
for _, row in top_targets.iterrows():
    station = row['start_station_name']
    month = row['month']

    # Isolating the specific station-month 'micro-market'
    subset = df[(df['start_station_name'] == station) & (df['month'] == month)]
    
    casual_rides = subset[subset['member_casual'] == 'casual']
    member_rides = subset[subset['member_casual'] == 'member']

    # If we don't have enough data for a comparison, we skip it. No 'junk' stats allowed.
    if len(casual_rides) < MIN_RIDES or len(member_rides) < MIN_RIDES:
        continue

    # Calculating hourly distributions (what percentage of rides happen at 8am, 9am, etc.)
    casual_dist = casual_rides['hour'].value_counts(normalize=True).sort_index()
    member_dist = member_rides['hour'].value_counts(normalize=True).sort_index()

    # Aligning the two groups into one table to calculate the correlation
    comparison = pd.concat([casual_dist, member_dist], axis=1).fillna(0)
    comparison.columns = ['casual_pct', 'member_pct']

    # Pearson Correlation: 1.0 means their schedules are identical.
    correlation = comparison['casual_pct'].corr(comparison['member_pct'])

    # Assigning a 'Verdict' based on how closely they mirror each other
    if correlation >= 0.85:
        verdict = "Strong Mirror (Ideal Target)"
    elif correlation >= 0.70:
        verdict = "Partial Mirror"
    else:
        verdict = "Weak Alignment"

    validation_results.append({
        'station': station,
        'month': month,
        'casual_count': len(casual_rides),
        'member_count': len(member_rides),
        'hourly_correlation': round(correlation, 3),
        'verdict': verdict
    })

# --- Finalizing ---
if not validation_results:
    print(" No valid mirrors found. Check your MIN_RIDES threshold.")
else:
    mirror_df = pd.DataFrame(validation_results).sort_values('hourly_correlation', ascending=False)
    mirror_df.to_csv(output_path, index=False)
    
    print("-" * 50)
    print(f"Validation complete! Results saved to: {output_path}")
    print("\nTop 5 Validated Conversion Zones:")
    print(mirror_df.head(5))