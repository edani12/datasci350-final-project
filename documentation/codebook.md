# Codebook
## Demographic Transitions and Healthcare Demand in East Asia
### DATASCI 350 - Final Project

---

## 1. Database Overview

**Database file:** `data/healthcare_demographics.db`  
**Format:** SQLite3  
**Time period:** 1990–2022  
**Countries:** 8  
**Total observations:** 264  

---

## 2. Tables

### 2.1 `countries`
Reference table containing country metadata.

| Column | Type | Description |
|---|---|---|
| `country_code` | TEXT (PK) | ISO 3-letter country code |
| `country_name` | TEXT | Full country name |
| `demographic_group` | TEXT | Classification by aging stage |

**Demographic group classifications:**

| Group | Countries | Description |
|---|---|---|
| Aged Economy | Japan | Population already severely aged, median age 48+ |
| Rapidly Aging | South Korea, China, Singapore | Fast transition, birth rates collapsing |
| Transitioning | Thailand, Vietnam | Mid-transition, improving health outcomes |
| Young Economy | Indonesia | Still relatively young population |
| Benchmark | United States | High-income comparator country |

---

### 2.2 `indicators`
Core data table containing all three WDI indicators.

| Column | Type | Description | Source |
|---|---|---|---|
| `id` | INTEGER (PK) | Auto-incremented row identifier | Generated |
| `country_code` | TEXT (FK) | References `countries.country_code` | World Bank |
| `year` | INTEGER | Calendar year (1990–2022) | World Bank |
| `life_expectancy` | REAL | Life expectancy at birth in years | World Bank WDI |
| `under5_mortality` | REAL | Deaths per 1,000 live births before age 5 | World Bank WDI |
| `adolescent_fertility` | REAL | Births per 1,000 women aged 15-19 | World Bank WDI |
| `decade` | TEXT | Decade label (e.g. '1990s') | Derived |

---

### 2.3 `combined_indicators`
Raw merged table loaded directly from Python download script.
Used as source for SQL cleaning pipeline.

---

## 3. Views

### 3.1 `clean_data`
Main analysis view joining `indicators` and `countries`.
Used as primary data source for all Python visualisations.

### 3.2 `summary_stats`
Average, min, and max of all three indicators per country
across the full 1990–2022 period.

### 3.3 `decade_averages`
Average of all three indicators per country per decade
(1990s, 2000s, 2010s, 2020s).

### 3.4 `improvement`
1990 vs 2022 comparison showing absolute change in each
indicator per country over the full study period.

### 3.5 `volatility`
Variance of each indicator per country across all years.
Higher variance = less stable demographic trajectory.

### 3.6 `rankings_2022`
Country rankings by each indicator in 2022 using
SQL window function RANK() OVER().

### 3.7 `group_averages`
Average indicators by demographic group per decade.
Used for group-level trend analysis.

---

## 4. World Bank Indicator Codes

| Indicator | Code | Unit | Source |
|---|---|---|---|
| Life expectancy at birth | `SP.DYN.LE00.IN` | Years | UN Population Division |
| Under-5 mortality rate | `SH.DYN.MORT` | Per 1,000 live births | UNICEF/WHO/World Bank |
| Adolescent fertility rate | `SP.ADO.TFRT` | Per 1,000 women aged 15-19 | UN Population Division |

---

## 5. Countries

| Code | Country | Region | Demographic Group |
|---|---|---|---|
| JPN | Japan | East Asia | Aged Economy |
| KOR | South Korea | East Asia | Rapidly Aging |
| CHN | China | East Asia | Rapidly Aging |
| SGP | Singapore | Southeast Asia | Rapidly Aging |
| THA | Thailand | Southeast Asia | Transitioning |
| VNM | Vietnam | Southeast Asia | Transitioning |
| IDN | Indonesia | Southeast Asia | Young Economy |
| USA | United States | North America | Benchmark |

---

## 6. Data Quality Notes

- All 264 observations are complete with zero missing values
- Life expectancy values are rounded to 2 decimal places
- Under-5 mortality values are rounded to 2 decimal places
- Adolescent fertility values are rounded to 2 decimal places
- Indonesia shows a dip in life expectancy around 2004
  reflecting the Indian Ocean tsunami (December 2004)
- United States shows a dip in life expectancy in 2020-2021
  reflecting excess mortality during the COVID-19 pandemic
- Data sourced directly from World Bank API using wbgapi
  package, accessed April 2026