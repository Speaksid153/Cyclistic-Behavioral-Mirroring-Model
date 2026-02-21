<div align="center">

#  Cyclistic: Behavioral Mirroring Model

### *Strategic Member Conversion via Behavioral DNA*

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Pandas](https://img.shields.io/badge/Pandas-2.0+-150458?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org)
[![Power BI](https://img.shields.io/badge/Power_BI-Dashboard-F2C811?style=for-the-badge&logo=powerbi&logoColor=black)](https://powerbi.microsoft.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](LICENSE)

*A data-driven framework that identifies high-conversion opportunity stations by mirroring casual rider behavior against established member commuting patterns.*

---

</div>

##  Project Overview

Traditional bike-share marketing targets **high-traffic tourist stations** for membership conversionn a brute-force approach with low ROI. This project takes a fundamentally different approach.

The **Behavioral Mirroring Model** shifts the focus from **volume** to **velocity of habit**. By constructing hourly ridership "DNA profiles" for every station, the model identifies locations where casual riders already exhibit the **"Twin Peaks"** commuting pattern (8 AM and 5 PM rush-hour spikes) characteristic of existing annual members.

These stations—termed **Strategic Anchors**—represent the highest-probability conversion targets because casual riders there already *behave* like members. They just haven't converted yet.

###  Business Question
> *How do annual members and casual riders use Cyclistic bikes differently, and how can we design a marketing strategy to convert casual riders into annual members?*

---

## Key Insights & Results

The model segments Chicago's 1,500+ bike stations into three actionable portfolio categories:

| Category | Description | Action |
|---|---|---|
| **✅ Confirmed Anchors** | Stations where casual riders consistently mirror member commuting DNA | Priority conversion targets |
| **🔶 High-Potential Emerging** | Stations showing intermittent mirroring signals | Monitor & nurture |
| **❌ Inconsistent / Noise** | Tourist-heavy stations with no commuting signal | Deprioritize |

### Core Findings

- **67% Member Share** during peak hours at Anchor stations — the optimal window for on-site activation campaigns
- **Twin Peaks Signal** validated across 13 months of trip data (Dec 2024 – Dec 2025)
- **Pearson Correlation** confirms statistically significant behavioral similarity between casual and member profiles at Anchor stations

###  Visualizations

| | |
|---|---|
| ![Strategic Anchor Map](results/behavioral_anchor_map.png) | ![Hourly DNA Profiles](results/anchor_vs_noise_dna.png) |
| *Geographic distribution of Strategic Anchors across Chicago* | *Hourly ridership DNA: Anchor stations vs. Noise stations* |
| ![Top Conversion Targets](results/top_anchor_leaderboard.png) | ![Portfolio Distribution](results/portfolio_distribution.png) |
| *Top-ranked stations by conversion potential* | *Portfolio segmentation breakdown* |

---

## Interactive Dashboard

> **File:** [`Cyclistic_Dashboard.pbix`](Cyclistic_Dashboard.pbix)

A fully interactive **Power BI Dashboard** accompanies this analysis, providing stakeholders with a dynamic, drill-down view of the findings.

> **Requirement:** [Power BI Desktop](https://powerbi.microsoft.com/desktop/) (free) is required to open and interact with the `.pbix` file.

---

##  Analytics Pipeline Architecture

The analysis is powered by a modular **6-stage Python pipeline**, with additional scripts for validation and geospatial analysis:


| Stage | Script | Purpose |
|:---:|---|---|
| 1 | `pipeline.py` | Data ingestion, cleaning, schema normalization, and feature engineering |
| 2 | `habitual_analysis.py` | Calculates station-level "Routine Scores" based on rush-hour consistency |
| 3 | `behavioral_refinement.py` | Normalizes scores and applies mirror-verdict classification logic |
| 4 | `station_segmentation.py` | Finalizes portfolio categorization (Anchors vs. Emerging vs. Noise) |
| 5 | `mirror_correlation.py` | Validates high-value targets via Pearson correlation analysis |
| 6 | `generate_visuals.py` | Produces production-ready charts and maps for stakeholder review |

### Supporting Scripts

| Script | Purpose |
|---|---|
| `geospatial_analysis.py` | Spatial metrics and geographic clustering analysis |
| `data_integrity_check.py` | Pre-pipeline data quality validation |
| `reliability_test.py` | Statistical reliability testing of model outputs |
| `statistical_validation.py` | Hypothesis testing and p-value validation |

---

##  Repository Structure

```
DIVVY PROJECT/
├── Cyclistic_Dashboard.pbix
├── README.md
├── .gitignore
├── Scripts/
│   ├── pipeline.py
│   ├── habitual_analysis.py
│   ├── behavioral_refinement.py
│   ├── station_segmentation.py
│   ├── mirror_correlation.py
│   ├── generate_visuals.py
│   ├── geospatial_analysis.py
│   ├── data_integrity_check.py
│   ├── reliability_test.py
│   └── statistical_validation.py
├── data/
│   ├── raw/
│   └── processed/
└── results/
```

---


##  Execution Guide

### Prerequisites

- **Python 3.10+**
- **Power BI Desktop** (for dashboard interaction)

### 1. Install Dependencies

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
*Created by [Your Name/Team Name]*
