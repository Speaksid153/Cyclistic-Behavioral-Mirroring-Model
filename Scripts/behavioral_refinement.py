import pandas as pd
from pathlib import Path

# --- Setup Paths ---
DATA_DIR = Path("./data/processed")

def run_behavioral_refinement():
    input_path = DATA_DIR / "habitual_metrics.csv"
    output_path = DATA_DIR / "refined_behavioral_scores.csv"

    if not input_path.exists():
        print(f"❌ Error: {input_path} not found. Run habitual_analysis.py first.")
        return

    df = pd.read_csv(input_path)
    
    # --- TIGHTENED LOGIC ---
    # We are raising the bar to filter out leisure-heavy stations
    def classify_mirror(rs):
        if rs >= 0.50: return "Strong Mirror"    # Up from 0.40
        elif rs >= 0.40: return "Moderate Mirror" # Up from 0.32
        elif rs >= 0.30: return "Weak Mirror"     # Up from 0.25
        else: return "Reject"

    df['mirror_verdict'] = df['routine_score'].apply(classify_mirror)

    # Normalization (Min-Max Scaling)
    df['normalized_RS'] = (
        (df['routine_score'] - df['routine_score'].min()) / 
        (df['routine_score'].max() - df['routine_score'].min())
    )

    df = df.sort_values(by='routine_score', ascending=False)
    df.to_csv(output_path, index=False)

    print("-" * 50)
    print(f"✅ SUCCESS: Refined scores saved to {output_path}")
    print("\nNew Marketing Breakdown:")
    print(df['mirror_verdict'].value_counts())

if __name__ == "__main__":
    run_behavioral_refinement()