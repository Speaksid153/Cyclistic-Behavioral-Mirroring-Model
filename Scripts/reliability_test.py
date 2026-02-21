import pandas as pd
from pathlib import Path

# --- Setup Paths ---
DATA_DIR = Path("./data/processed")

def run_reliability_test():
    input_path = DATA_DIR / "hourly_validation_metrics.csv"
    output_path = DATA_DIR / "behavioral_concentration_metrics.csv"

    if not input_path.exists():
        print(f"❌ Error: {input_path} not found. Run statistical_validation.py first.")
        return

    print("Starting Concentration Metrics Validation (The Behavioral Gap Test)...")
    hourly_df = pd.read_csv(input_path)
    results = []

    # --- Calculation Engine ---
    for segment in hourly_df['final_status'].unique():
        segment_data = hourly_df[hourly_df['final_status'] == segment]
        
        # Metric 1: Concentration (Top 2 hours sum) - identifies 'Rush Hour' intensity
        sorted_by_val = segment_data.sort_values(by='pct_of_daily_rides', ascending=False)
        top2_concentration = sorted_by_val.head(2)['pct_of_daily_rides'].sum()
        
        # Metric 2: Hourly Std Deviation - identifies 'Peakiness'
        std_dev = segment_data['pct_of_daily_rides'].std()
        
        results.append({
            "Segment": segment,
            "Top 2 Hour Concentration (%)": round(top2_concentration, 2),
            "Hourly Std Deviation": round(std_dev, 2)
        })

    metrics_df = pd.DataFrame(results)
    metrics_df.to_csv(output_path, index=False)

    # --- The "Behavioral Gap" Logic ---
    anchor_stats = metrics_df[metrics_df['Segment'] == 'Confirmed Behavioral Anchor']
    noise_stats = metrics_df[metrics_df['Segment'] == 'Inconsistent / Noise']

    if not anchor_stats.empty and not noise_stats.empty:
        a_conc = anchor_stats['Top 2 Hour Concentration (%)'].values[0]
        n_conc = noise_stats['Top 2 Hour Concentration (%)'].values[0]
        ratio = a_conc / n_conc
        
        print("\n" + "="*40)
        print(f"FINAL BEHAVIORAL GAP: {ratio:.2f}x")
        
        if ratio >= 1.5:
            print("DECISION: ELITE SEPARATION - Segmentation Validated.")
        elif ratio >= 1.25:
            print("DECISION: CLEAR SEPARATION - Habits identified.")
        else:
            print("DECISION: WEAK SEPARATION - Adjust Routine Score thresholds.")
        print("="*40)

if __name__ == "__main__":
    run_reliability_test()