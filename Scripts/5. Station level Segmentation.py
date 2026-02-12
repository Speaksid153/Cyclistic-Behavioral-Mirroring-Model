import pandas as pd
from pathlib import Path

print("Starting Step 4: Final Station Segmentation (Density-Dominant Model)")

# ==========================================
# PATH SETUP 
# ==========================================
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent

input_path = PROJECT_ROOT / "Data" / "Processed Datasets" / "refined_behavioral_scores.csv"
output_path = PROJECT_ROOT / "Data" / "Processed Datasets" / "station_behavior_segments.csv"

# ==========================================
# LOAD DATA
# ==========================================
df = pd.read_csv(input_path)

print(f"Loaded {len(df):,} station-month records.")

# ==========================================
# 1️. DENSITY SCORE
# % of months classified as Strong Mirror
# ==========================================
density_df = (
    df.groupby("start_station_name")["mirror_verdict"]
    .apply(lambda x: (x == "Strong Mirror").sum() / len(x))
    .reset_index(name="density_score")
)

print("Density score calculated.")

# ==========================================
# 2️. CONSISTENCY SCORE (Ranking only)
# Average Routine Score (RS) across months
# ==========================================
consistency_df = (
    df.groupby("start_station_name")["RS"]
    .mean()
    .reset_index(name="consistency_score")
)

print("Consistency score calculated.")

# ==========================================
# 3️. MERGE METRICS
# ==========================================
final_df = density_df.merge(consistency_df, on="start_station_name")

# ==========================================
# 4️. FINAL CLASSIFICATION (Density-Dominant)
# ==========================================
def classify(density):
    if density >= 0.40:
        return "Confirmed Behavioral Anchor"
    elif density >= 0.20:
        return "High-Potential Emerging"
    else:
        return "Inconsistent / Noise"

final_df["final_status"] = final_df["density_score"].apply(classify)

# ==========================================
# SAVE OUTPUT
# ==========================================
output_path.parent.mkdir(parents=True, exist_ok=True)
final_df.to_csv(output_path, index=False)

print("-" * 50)
print(f"Success. Final segments saved to:\n{output_path}")

print("\nFinal Portfolio Distribution:")
print(final_df["final_status"].value_counts())

print("\nTop Anchors (Sorted by Consistency):")
print(
    final_df[final_df["final_status"] == "Confirmed Behavioral Anchor"]
    .sort_values("consistency_score", ascending=False)
    .head(10)
)
