# Demographic Transitions and Healthcare Demand in East Asia

**DATASCI 350 - Data Science Computing | Final Project**

## Authors
- Eshaan Dani — 2549526
- Nikhil Makker — 2549325
- Connor Lee — [Emory ID]
- Ihan Do — 2613107
- [Teammate 5] — [Emory ID]

## Research Question
How have life expectancy, child mortality, and fertility trends diverged 
across East Asian economies from 1990 to 2022, and what do these demographic 
trajectories imply for future healthcare services demand?

## Project Structure

```
datasci350-final-project/
├── README.md
├── report.qmd              # Quarto source document
├── report.html             # Rendered HTML report
├── report.pdf              # Rendered PDF report
├── references.bib          # Bibliography
├── requirements.txt        # Python dependencies
├── data/                   
│   ├── combined_indicators.csv
│   ├── life_expectancy.csv
│   ├── under5_mortality.csv
│   ├── adolescent_fertility.csv
│   └── healthcare_demographics.db
├── documentation/          
│   ├── codebook.md
│   ├── er_diagram.png
│   └── er_diagram.py
├── figures/                
│   ├── 01_life_expectancy.png
│   ├── 02_under5_mortality.png
│   ├── 03_adolescent_fertility.png
│   ├── 04_improvement.png
│   ├── 05_scorecard_heatmap.png
│   ├── 06_group_trends.png
│   └── 07_scatter_2022.png
└── scripts/                
    ├── 01_download_data.py
    ├── 02_clean_data.sql
    ├── 03_descriptive_stats.sql
    └── 04_analysis.py
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
