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
pip install pandas numpy seaborn matplotlib scipy folium
```

### 2. Add Raw Data

Place Divvy trip data CSVs into the `data/raw/` directory. Data is available from the [Divvy Trip Data Portal](https://divvy-tripdata.s3.amazonaws.com/index.html).

### 3. Run the Full Pipeline

Run the following scripts in stages:

```powershell
cd Scripts
python pipeline.py                  # Stage 1
python habitual_analysis.py         # Stage 2
python behavioral_refinement.py     # Stage 3
python station_segmentation.py      # Stage 4
python mirror_correlation.py        # Stage 5
python generate_visuals.py          # Stage 6
```

### 4. Open the Dashboard

Open `Cyclistic_Dashboard.pbix` in Power BI Desktop to explore the interactive visualizations.

---

##  Strategic Framework

| Concept | Description |
|---|---|
| **Twin Peaks Signal** | Ridership concentrations during the 8 AM and 5 PM windows — the behavioral fingerprint of habitual commuters |
| **Behavioral DNA Profile** | A 24-hour hourly ridership distribution curve unique to each station, used to classify rider behavior |
| **Mirror Verdict** | A station passes when its casual rider DNA profile statistically mirrors the member DNA profile |
| **Density vs. Consistency** | Stations are ranked not just by trip volume, but by how *reliably* they maintain mirroring status over time |
| **Conversion Window** | Data shows 67% member share during peak hours at Anchor stations — the optimal time for on-site activation |

---

## 📐 Methodology

1. **Data Ingestion** — 13 months of Divvy trip records (~5.8M+ rides) are cleaned, normalized, and enriched with temporal features.
2. **Commute Detection** — Trips are flagged as commute rides based on time-of-day, day-of-week, and duration thresholds.
3. **Routine Scoring** — Each station receives a "Routine Score" measuring the concentration of commute-like behavior among casual riders.
4. **Behavioral Normalization** — Scores are scaled and compared against the member baseline to produce a mirror verdict.
5. **Portfolio Segmentation** — Stations are classified into Anchor / Emerging / Noise categories based on scoring thresholds.
6. **Statistical Validation** — Pearson correlation and reliability tests confirm the robustness of identified Anchor stations.
7. **Visualization & Dashboard** — Results are exported as production charts and loaded into an interactive Power BI dashboard.

---

## 📄 Data Source

This project uses publicly available trip data from **Divvy** (operated by Lyft), Chicago's bike-share system.

- **Source:** [Divvy Trip Data](https://divvy-tripdata.s3.amazonaws.com/index.html)
- **License:** Data provided under the [Divvy Data License Agreement](https://divvybikes.com/data-license-agreement)
- **Period:** December 2024 – December 2025 (13 months)

---

<div align="center">

*Built as part of the Google Data Analytics Professional Certificate Capstone Project.*

</div>
