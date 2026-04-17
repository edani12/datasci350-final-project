# Demographic Transitions and Healthcare Demand in East Asia

**DATASCI 350 - Data Science Computing | Final Project**

## Authors
- Eshaan Dani — 2549526
- Nikhil Makker — [Emory ID]
- Connor Lee — [Emory ID]
- [Teammate 4] — [Emory ID]
- [Teammate 5] — [Emory ID]

## Research Question
How have life expectancy, child mortality, and fertility trends diverged 
across East Asian economies from 1990 to 2022, and what do these demographic 
trajectories imply for future healthcare services demand?

## Project Structure

```
datasci350-final-project/
├── README.md
├── data/               # Raw and processed datasets
├── documentation/      # Codebook and ER diagram
├── figures/            # All plots and tables
├── scripts/            # SQL and Python analysis scripts
│   ├── 01_download_data.py
│   ├── 02_clean_data.sql
│   ├── 03_descriptive_stats.sql
│   └── 04_analysis.py
└── report.qmd          # Quarto report (main document)
```

## How to Reproduce

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Download the data
```bash
python scripts/01_download_data.py
```

### 3. Run SQL cleaning and descriptive statistics
```bash
sqlite3 data/healthcare_demographics.db < scripts/02_clean_data.sql
sqlite3 data/healthcare_demographics.db < scripts/03_descriptive_stats.sql
```

### 4. Run Python analysis
```bash
python scripts/04_analysis.py
```

### 5. Render the Quarto report
```bash
quarto render report.qmd
```

## Data Source
World Bank World Development Indicators (WDI)
- Life expectancy at birth (SP.DYN.LE00.IN)
- Under-5 mortality rate (SH.DYN.MORT)
- Adolescent fertility rate (SP.ADO.TFRT)

## Requirements
- Python 3.12+
- SQLite3
- Quarto 1.6+
- See requirements.txt for Python packages
