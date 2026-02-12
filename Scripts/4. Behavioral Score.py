import pandas as pd
from pathlib import Path

# --- Setup Paths ---

input_path = Path('Data/Processed Datasets/monthly_conversion_metrics.csv')
output_path = Path('Data/Processed Datasets/refined_behavioral_scores.csv')

print("Starting : Refining Behavioral Mirroring Categories...")

# --- Loading the Metrics ---
if not input_path.exists():
    print(f"Error: {input_path.name} not found.")
    print("Make sure to run 02_behavioral_analysis.py first!")
    exit()

df = pd.read_csv(input_path)
print(f"Data loaded successfully. Processing {len(df):,} station-month records.")


def classify_mirror(rs):
    if rs >= 0.40:
        return "Strong Mirror"   
    elif rs >= 0.32:
        return "Moderate Mirror"  # Good
    elif rs >= 0.25:
        return "Weak Mirror"      # Likely just accidental overlap
    else:
        return "Reject"           # Purely leisure or tourist-heavy spots

df['mirror_verdict'] = df['RS'].apply(classify_mirror)

# --- Normalizing the Routine Score ---
# This scales the RS between 0 and 1. 
# It's useful for later visualizations or if we want to combine this with other metrics.
df['normalized_RS'] = (
    (df['RS'] - df['RS'].min()) / 
    (df['RS'].max() - df['RS'].min())
)

# Sorting so the 'Elite' targets are right at the top of the file
df = df.sort_values(by='RS', ascending=False)

# --- Saving the Results ---
# Making sure the folder exists before we try to write to it
output_path.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(output_path, index=False)

print("-" * 50)
print(f"Refinement complete. Saved to: {output_path}")

# Quick reality check on the numbers
print("\nFinal Breakdown of Station Targets:")
print(df['mirror_verdict'].value_counts())