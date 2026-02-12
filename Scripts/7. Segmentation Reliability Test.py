import pandas as pd
from pathlib import Path
import sys

# --- Setup GitHub-Ready Paths ---
# This finds the root project folder regardless of whose computer it is on
BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_PATH = BASE_DIR / "Data" / "Processed Datasets" / "casual_anchor_vs_noise_hourly.csv"
OUTPUT_PATH = BASE_DIR / "Data" / "Processed Datasets" / "behavioral_concentration_metrics.csv"

print("Starting Concentration Metrics Validation...")

# --- Load Data ---
if not INPUT_PATH.exists():
    print(f"CRITICAL ERROR: Could not find dataset at {INPUT_PATH}")
    print("Check your folder structure. Expected: Project_Root/Data/Processed Datasets/")
    sys.exit(1)

hourly_df = pd.read_csv(INPUT_PATH)
results = []

# --- Calculation Engine ---
for segment in hourly_df['final_status'].unique():
    segment_data = hourly_df[hourly_df['final_status'] == segment]
    
    # Identify the 'peaks'
    sorted_by_val = segment_data.sort_values(by='percentage', ascending=False)
    
    # Metric 1: Concentration (Top 2 hours sum)
    top2_concentration = sorted_by_val.head(2)['percentage'].sum()
    
    # Metric 2: Hourly Std Deviation (Peakiness)
    std_dev = segment_data['percentage'].std()
    
    results.append({
        "Segment": segment,
        "Top 2 Hour Concentration (%)": round(top2_concentration, 2),
        "Hourly Std Deviation": round(std_dev, 2)
    })

metrics_df = pd.DataFrame(results)

# --- Analysis & Comparison ---
print("\n" + "="*40)
print("STATISTICAL VALIDATION RESULTS")
print("="*40)
print(metrics_df.to_string(index=False))

# Ensure output directory exists and save
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
metrics_df.to_csv(OUTPUT_PATH, index=False)
print(f"\nResults saved to: {OUTPUT_PATH}")

# --- The "Behavioral Gap" Logic ---
anchor_stats = metrics_df[metrics_df['Segment'] == 'Confirmed Behavioral Anchor']
noise_stats = metrics_df[metrics_df['Segment'] == 'Inconsistent / Noise']

if not anchor_stats.empty and not noise_stats.empty:
    a_conc = anchor_stats['Top 2 Hour Concentration (%)'].values[0]
    n_conc = noise_stats['Top 2 Hour Concentration (%)'].values[0]
    ratio = a_conc / n_conc
    
    print("\n" + "-"*40)
    print(f"FINAL BEHAVIORAL GAP: {ratio:.2f}x")
    
    if ratio >= 1.5:
        print("DECISION: ELITE SEPARATION - Segmentation Validated.")
    elif ratio >= 1.25:
        print("DECISION: CLEAR SEPARATION - Habits identified.")
    else:
        print("DECISION: WEAK SEPARATION - Adjust Routine Score thresholds.")
    print("-"*40)