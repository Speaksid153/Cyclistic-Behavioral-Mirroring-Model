import pandas as pd
from pathlib import Path

# =========================
# 1. PATH SETUP (PORTABLE)
# =========================
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent 

input_path = PROJECT_ROOT / 'Data' / 'Processed Datasets' / 'cyclistic_casual_only.csv'
output_path = PROJECT_ROOT / 'Data' / 'Processed Datasets' / 'monthly_conversion_metrics.csv'

print("Starting Cyclistic Casual Habitual Conversion Analysis...")

# Safety check
if not input_path.exists():
    print(f"❌ ERROR: Missing {input_path}. Did you run script #2?")
    exit()

# =========================
# 2. DATA LOADING & CLEANING
# =========================
df = pd.read_csv(input_path)
print(f"Step 1: Data loaded. Total rows: {len(df):,}")

# Drop missing start stations (can't analyze behavior without location)
casuals = df.dropna(subset=['start_station_name']).copy()
print(f"Step 2: Dropped rows with missing stations. Rows remaining: {len(casuals):,}")

# =========================
# 3. FREQUENCY GATE
# =========================
# Why? We only care about stations where casual riders appear consistently.
casuals['station_month_count'] = casuals.groupby(['start_station_name', 'month'])['hour'].transform('count')
VOLUME_FLOOR = 100
casuals = casuals[casuals['station_month_count'] >= VOLUME_FLOOR]
print(f"Step 3: Applied Frequency Gate (>= {VOLUME_FLOOR} rides/month). Rows remaining: {len(casuals):,}")

# =========================
# 4. HOURLY CONSISTENCY (Ch)
# =========================
# Logic: If a large % of rides happen in the same 2-hour window, it's a routine.
casuals['hour_bin'] = (casuals['hour'] // 2) * 2
bin_counts = casuals.groupby(['start_station_name', 'month', 'hour_bin']).size().reset_index(name='bin_vol')
total_vol = bin_counts.groupby(['start_station_name', 'month'])['bin_vol'].transform('sum')
bin_counts['bin_share'] = bin_counts['bin_vol'] / total_vol

# Ch = The percentage of the busiest 2-hour block
ch_scores = bin_counts.groupby(['start_station_name', 'month'])['bin_share'].max().reset_index(name='Ch')
print("Step 4: Hourly consistency (Ch) calculated.")

# =========================
# 5. MID-WEEK FOCUS (Cd)
# =========================
# Logic: Casuals riding Tue/Wed/Thu are likely commuting.
midweek_names = ['Tuesday', 'Wednesday', 'Thursday']
casuals['is_midweek'] = casuals['day_of_week'].isin(midweek_names).astype(int)
cd_scores = casuals.groupby(['start_station_name', 'month'])['is_midweek'].mean().reset_index(name='Cd')
print("Step 5: Mid-week focus (Cd) calculated.")

# =========================
# 6. ROUTINE SCORE (RS) & TIERING
# =========================
results = ch_scores.merge(cd_scores, on=['start_station_name', 'month'])

# Weighted Score: 60% Hourly Consistency, 40% Mid-week focus
results['RS'] = (results['Ch'] * 0.6) + (results['Cd'] * 0.4)

def assign_tier(rs):
    if rs >= 0.35: return 'Strong'
    elif rs >= 0.25: return 'Emerging'
    else: return 'Low'

results['Tier'] = results['RS'].apply(assign_tier)
results = results.sort_values(by='RS', ascending=False)

# =========================
# 7. SAVE RESULTS
# =========================
output_path.parent.mkdir(parents=True, exist_ok=True)
results.to_csv(output_path, index=False)

print("-" * 40)
print(f"ANALYSIS COMPLETE. Results saved to: {output_path}")
print("\nTOP 10 CONVERSION TARGETS (By Routine Score):")
print(results.head(10))