import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path

# --- Setup Paths (The Robust Way) ---
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
INPUT_PATH = PROJECT_ROOT / "Data" / "Processed Datasets" / "station_behavior_segments.csv"
SAVE_PATH = PROJECT_ROOT / "Results" / "behavioral_anchor_map.png"

print("Generating Strategic Behavioral Anchor Map...")

if not INPUT_PATH.exists():
    print(f"ERROR: File not found at {INPUT_PATH}")
    exit()

df = pd.read_csv(INPUT_PATH)

# Visualization logic
plt.figure(figsize=(10, 8))
palette = {"Confirmed Behavioral Anchor": "#2ecc71", "High-Potential Emerging": "#f1c40f", "Inconsistent / Noise": "#bdc3c7"}

sns.scatterplot(data=df, x="density_score", y="consistency_score", hue="final_status", palette=palette, s=110, alpha=0.75)

# Decision Thresholds
plt.axvline(x=0.35, color="#e74c3c", linestyle="--", alpha=0.6)
plt.axhline(y=0.35, color="#e74c3c", linestyle="--", alpha=0.6)

plt.title("Strategic Segmentation: Density vs. Consistency", fontsize=16, pad=25)
plt.xlabel("Density Score (% Months as Strong Mirror)")
plt.ylabel("Mean Routine Strength")

SAVE_PATH.parent.mkdir(parents=True, exist_ok=True)
plt.savefig(SAVE_PATH, dpi=300, bbox_inches="tight")
print(f"SUCCESS: Map saved to {SAVE_PATH}")
plt.show()