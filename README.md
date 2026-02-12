# Cyclistic Bike-Share Analysis: From Casual to Committed 

## Project Overview
This project analyzes historical bike trip data from **Cyclistic**, a fictional bike-share company in Chicago. The goal is to understand how casual riders and annual members use Cyclistic bikes differently. These insights will be used to design a new marketing strategy to convert casual riders into annual members.

The analysis follows a data analysis process: **Ask, Prepare, Process, Analyze, Share, and Act**.

##  Project Structure

```
DIVVY PROJECT/
├── Data/
│   ├── Raw Datasets/          # Original CSV files (e.g., 202301-divvy-tripdata.csv)
│   └── Processed Datasets/    # Cleaned and intermediate datasets
├── Results/                   # Output visualizations (PNG charts)
├── Scripts/                   # Python scripts and Jupyter Notebooks for analysis
│   ├── Extra Validation/      # Additional validation scripts
│   └── [Numbered Scripts/Notebooks]
└── README.md                  # Project documentation
```

##  Key Features of the Analysis

1.  **Data Cleaning & Processing**: Merges monthly datasets, handles missing values, and creates new features (ride length, day of week, etc.).
2.  **Behavioral Segmentation**: Uses a "Habitual Score" (Routine Score) to identify casual riders who exhibit member-like behavior (commuting, consistent usage).
3.  **Station-Level Analysis**: Segments stations into "Behavioral Anchors" (high conversion potential) and "Noise".
4.  **Statistical Validation**: Validates the segmentation using concentration metrics and hourly ride distribution comparisons.
5.  **Visualizations**: Generates professional charts to communicate findings effectively.

## Requirements

To run the analysis, you need Python and the following libraries:

```bash
pip install pandas matplotlib seaborn pathlib
```

##  How to Run the Analysis

The analysis is broken down into a sequence of numbered scripts/notebooks. Run them in order:

1.  **`1_Master_dataset_cleaned.ipynb`**: Merges raw data and performs initial cleaning.
2.  **`2_Causal_Members_only_Filter.ipynb`**: Creates a focused dataset of casual riders.
3.  **`3_Habitual_score.ipynb`**: Calculates habitual scores for stations based on ride frequency and consistency.
4.  **`4_Behavioral_Score.ipynb`**: Refines scores into "Strong Mirror", "Moderate Mirror", etc.
5.  **`5_Station_level_Segmentation.ipynb`**: Final segmentation of stations into Anchors vs. Noise.
6.  **`6_Hourly_statistical_Validation.ipynb`**: Prepares data for hourly comparison validation.
7.  **`7_Segmentation_Reliability_Test.ipynb`**:Calculates statistical metrics to validate the segments.
8.  **`8_Portfolio_distribution.ipynb`**: Visualizes the distribution of station segments.
9.  **`9_Classification_graph.ipynb`**: Visualizes Density vs. Consistency.
10. **`10_Anchor_vs_Noise_Hourly_Comparison.ipynb`**: Creates a DNA chart comparing hourly patterns.
11. **`11_Actionable_insights.ipynb`**: Identifies the top 10 high-value conversion targets.

### Extra Validation
Located in `Scripts/Extra Validation/`:
*   `Extra_Validation_1_Casual_only_validation.ipynb`: Validates the quality of the casual-only dataset.
*   `Extra_Validation_2_Mirror_validation.ipynb`: validation of member-mirroring behavior.

## Results

The analysis produces several key visualizations in the `Results/` folder, including:
*   `portfolio_distribution.png`: Breakdown of station segments.
*   `behavioral_anchor_map.png`: Strategic map of station density vs. consistency.
*   `anchor_vs_noise_dna.png`: Hourly ride comparison showing the "commuter signal".
*   `top_10_anchor_stations.png`: Leaderboard of top stations for marketing targeting.

## Key Findings (Example)
*   **Behavioral Anchors**: A subset of stations shows strong "commuter" patterns among casual riders, mirroring annual members.
*   **Actionable Strategy**: Marketing efforts should be targeted at these specific "Behavioral Anchor" stations during peak commuting hours (7-9 AM, 4-6 PM) to maximize conversion rates.

---
*Created by Siddharth.R
