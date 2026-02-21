import pandas as pd
from pathlib import Path

# --- Setup Paths ---
DATA_DIR = Path("./data/processed")

def run_station_segmentation():
    input_path = DATA_DIR / "refined_behavioral_scores.csv"
    output_path = DATA_DIR / "station_behavior_segments.csv"

    if not input_path.exists():
        print(f"❌ Error: {input_path} not found.")
        return

    df = pd.read_csv(input_path)

    # 1. Density Score
    density_df = (
        df.groupby("start_station_name")["mirror_verdict"]
        .apply(lambda x: (x == "Strong Mirror").sum() / len(x))
        .reset_index(name="density_score")
    )

    # 2. Consistency Score
    consistency_df = (
        df.groupby("start_station_name")["routine_score"]
        .mean()
        .reset_index(name="consistency_score")
    )

    final_df = density_df.merge(consistency_df, on="start_station_name")

    # --- TIGHTENED LOGIC ---
    # Raising the consistency requirement for the portfolio
    def classify_station(density):
        if density >= 0.60:  # Must be a Strong Mirror 60%+ of the time
            return "Confirmed Behavioral Anchor"
        elif density >= 0.30: 
            return "High-Potential Emerging"
        else:
            return "Inconsistent / Noise"

    final_df["final_status"] = final_df["density_score"].apply(classify_station)
    final_df = final_df.sort_values("consistency_score", ascending=False)
    final_df.to_csv(output_path, index=False)

    print("-" * 50)
    print(f"✅ SUCCESS: High-density segments saved to {output_path}")
    print("\nNew Portfolio Distribution:")
    print(final_df["final_status"].value_counts())

if __name__ == "__main__":
    run_station_segmentation()