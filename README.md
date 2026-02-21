<div align="center">

#  Cyclistic: Behavioral Mirroring Model

### *Strategic Member Conversion via Behavioral DNA*

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Pandas](https://img.shields.io/badge/Pandas-2.0+-150458?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org)
[![Jupyter](https://img.shields.io/badge/Jupyter-Notebooks-F37626?style=for-the-badge&logo=jupyter&logoColor=white)](https://jupyter.org)
[![Power BI](https://img.shields.io/badge/Power_BI-Dashboard-F2C811?style=for-the-badge&logo=powerbi&logoColor=black)](https://powerbi.microsoft.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](LICENSE)

*A data-driven framework that identifies high-conversion opportunity stations by mirroring casual rider behavior against established member commuting patterns.*

---

</div>

##  Project Overview

Traditional bike-share marketing targets **high-traffic tourist stations** for membership conversion — a brute-force approach with low ROI. This project takes a fundamentally different approach.

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

## Interactive Dashboard

> **File:** [`Cyclistic_Dashboard.pbix`](Cyclistic_Dashboard.pbix)

A fully interactive **Power BI Dashboard** accompanies this analysis, providing stakeholders with a dynamic, drill-down view of the findings.

> **Requirement:** [Power BI Desktop](https://powerbi.microsoft.com/desktop/) (free) is required to open and interact with the `.pbix` file.

---

##  Analytics Pipeline Architecture

The analysis is powered by a modular **6-stage Jupyter Notebook pipeline**, with additional notebooks for validation and geospatial analysis. All notebooks are located in the `Notebooks/` directory.

### Core Pipeline

| Stage | Notebook | Purpose |
|:---:|---|---|
| 1 | `pipeline.ipynb` | Data ingestion, cleaning, schema normalization, and feature engineering |
| 2 | `habitual_analysis.ipynb` | Calculates station-level "Routine Scores" based on rush-hour consistency |
| 3 | `behavioral_refinement.ipynb` | Normalizes scores and applies mirror-verdict classification logic |
| 4 | `station_segmentation.ipynb` | Finalizes portfolio categorization (Anchors vs. Emerging vs. Noise) |
| 5 | `mirror_correlation.ipynb` | Validates high-value targets via Pearson correlation analysis |
| 6 | `generate_visuals.ipynb` | Produces production-ready charts and maps for stakeholder review |

### Validation & Supporting Notebooks

| Notebook | Purpose |
|---|---|
| `geospatial_analysis.ipynb` | Spatial metrics and geographic clustering analysis |
| `data_integrity_check.ipynb` | Pre-pipeline data quality validation |
| `reliability_test.ipynb` | Statistical reliability testing of model outputs |
| `statistical_validation.ipynb` | Hypothesis testing and p-value validation |

---

##  Repository Structure

```
DIVVY PROJECT/
├── Notebooks/
│   ├── pipeline.ipynb
│   ├── habitual_analysis.ipynb
│   ├── behavioral_refinement.ipynb
│   ├── station_segmentation.ipynb
│   ├── mirror_correlation.ipynb
│   ├── generate_visuals.ipynb
│   ├── geospatial_analysis.ipynb
│   ├── data_integrity_check.ipynb
│   ├── reliability_test.ipynb
│   └── statistical_validation.ipynb
├── data/
│   ├── raw/
│   └── processed/
├── results/
├── Cyclistic_Dashboard.pbix
├── LICENSE
└── README.md
```

---

##  Execution Guide

### Prerequisites

- **Python 3.10+**
- **Jupyter Notebook** or **JupyterLab**
- **Power BI Desktop** (for dashboard interaction)

### 1. Install Dependencies

```bash
pip install pandas matplotlib seaborn jupyter
```

### 2. Run the Pipeline

Launch Jupyter and execute the notebooks **in order** from the `Notebooks/` directory:

```bash
jupyter notebook Notebooks/
```

| Order | Notebook | Description |
|:---:|---|---|
| 1 | `pipeline.ipynb` | Merges raw data and performs initial cleaning |
| 2 | `habitual_analysis.ipynb` | Calculates habitual scores for stations |
| 3 | `behavioral_refinement.ipynb` | Refines scores into mirror-verdict categories |
| 4 | `station_segmentation.ipynb` | Final segmentation into Anchors vs. Noise |
| 5 | `mirror_correlation.ipynb` | Pearson correlation validation of targets |
| 6 | `generate_visuals.ipynb` | Generates all production-ready visualizations |

### 3. Validation Notebooks (Optional)

Run these independently for additional quality checks:

- `data_integrity_check.ipynb` — Pre-pipeline data quality validation
- `geospatial_analysis.ipynb` — Spatial metrics and geographic clustering
- `reliability_test.ipynb` — Statistical reliability of model outputs
- `statistical_validation.ipynb` — Hypothesis testing and p-value validation

---

## Results

The analysis produces key visualizations in the `results/` folder:

| File | Description |
|---|---|
| `behavioral_anchor_map.png` | Strategic map of station density vs. consistency |
| `anchor_vs_noise_dna.png` | Hourly ride comparison showing the "commuter signal" |
| `top_anchor_leaderboard.png` | Leaderboard of top stations for marketing targeting |
| `portfolio_distribution.png` | Breakdown of station segments |

## Key Findings

- **Behavioral Anchors**: A subset of stations shows strong "commuter" patterns among casual riders, mirroring annual members.
- **Actionable Strategy**: Marketing efforts should be targeted at these specific "Behavioral Anchor" stations during peak commuting hours (7–9 AM, 4–6 PM) to maximize conversion rates.

---
