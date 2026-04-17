-- 02_clean_data.sql
-- SQL data cleaning script for healthcare demographics analysis
-- Creates properly structured tables with primary/foreign keys
-- and performs all necessary cleaning steps

-- ── 1. CREATE COUNTRIES REFERENCE TABLE ─────────────────────────────────────

DROP TABLE IF EXISTS countries;
CREATE TABLE countries (
    country_code    TEXT    NOT NULL PRIMARY KEY,
    country_name    TEXT    NOT NULL,
    demographic_group TEXT  NOT NULL
);

INSERT INTO countries (country_code, country_name, demographic_group) VALUES
    ('JPN', 'Japan',         'Aged Economy'),
    ('KOR', 'South Korea',   'Rapidly Aging'),
    ('CHN', 'China',         'Rapidly Aging'),
    ('SGP', 'Singapore',     'Rapidly Aging'),
    ('THA', 'Thailand',      'Transitioning'),
    ('VNM', 'Vietnam',       'Transitioning'),
    ('IDN', 'Indonesia',     'Young Economy'),
    ('USA', 'United States', 'Benchmark');

-- ── 2. CREATE CLEANED INDICATORS TABLE ──────────────────────────────────────

DROP TABLE IF EXISTS indicators;
CREATE TABLE indicators (
    id                      INTEGER PRIMARY KEY AUTOINCREMENT,
    country_code            TEXT    NOT NULL,
    year                    INTEGER NOT NULL,
    life_expectancy         REAL,
    under5_mortality        REAL,
    adolescent_fertility    REAL,
    decade                  TEXT    NOT NULL,
    FOREIGN KEY (country_code) REFERENCES countries(country_code)
);

-- ── 3. POPULATE FROM COMBINED RAW DATA ──────────────────────────────────────

INSERT INTO indicators (
    country_code,
    year,
    life_expectancy,
    under5_mortality,
    adolescent_fertility,
    decade
)
SELECT
    country_code,
    year,
    -- Round to 2 decimal places for cleanliness
    ROUND(life_expectancy, 2),
    ROUND(under5_mortality, 2),
    ROUND(adolescent_fertility, 2),
    decade
FROM combined_indicators
-- Only include years 1990-2022
WHERE year BETWEEN 1990 AND 2022
-- Only include our 8 countries
AND country_code IN ('JPN','KOR','CHN','SGP','THA','VNM','IDN','USA');

-- ── 4. VERIFY ROW COUNTS ─────────────────────────────────────────────────────

SELECT
    'countries'  AS table_name,
    COUNT(*)     AS row_count
FROM countries
UNION ALL
SELECT
    'indicators' AS table_name,
    COUNT(*)     AS row_count
FROM indicators;

-- ── 5. CHECK FOR ANY REMAINING NULLS ────────────────────────────────────────

SELECT
    country_code,
    SUM(CASE WHEN life_expectancy      IS NULL THEN 1 ELSE 0 END) AS null_life_exp,
    SUM(CASE WHEN under5_mortality     IS NULL THEN 1 ELSE 0 END) AS null_mortality,
    SUM(CASE WHEN adolescent_fertility IS NULL THEN 1 ELSE 0 END) AS null_fertility
FROM indicators
GROUP BY country_code
ORDER BY country_code;

-- ── 6. VERIFY DATE RANGE ─────────────────────────────────────────────────────

SELECT
    country_code,
    MIN(year) AS first_year,
    MAX(year) AS last_year,
    COUNT(*)  AS total_years
FROM indicators
GROUP BY country_code
ORDER BY country_code;

-- ── 7. CREATE CLEANED VIEW FOR ANALYSIS ─────────────────────────────────────

DROP VIEW IF EXISTS clean_data;
CREATE VIEW clean_data AS
SELECT
    i.id,
    i.country_code,
    c.country_name,
    c.demographic_group,
    i.year,
    i.decade,
    i.life_expectancy,
    i.under5_mortality,
    i.adolescent_fertility
FROM indicators i
JOIN countries c
    ON i.country_code = c.country_code
ORDER BY i.country_code, i.year;

-- Confirm view works
SELECT COUNT(*) AS total_rows FROM clean_data;