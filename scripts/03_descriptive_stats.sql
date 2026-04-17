-- 03_descriptive_stats.sql
-- Descriptive statistics for healthcare demographics analysis
-- All results feed directly into the Quarto report

-- ── 1. OVERALL SUMMARY STATISTICS PER COUNTRY ───────────────────────────────

DROP VIEW IF EXISTS summary_stats;
CREATE VIEW summary_stats AS
SELECT
    c.country_name,
    c.demographic_group,
    -- Life expectancy stats
    ROUND(AVG(i.life_expectancy), 2)            AS avg_life_exp,
    ROUND(MIN(i.life_expectancy), 2)            AS min_life_exp,
    ROUND(MAX(i.life_expectancy), 2)            AS max_life_exp,
    -- Under-5 mortality stats
    ROUND(AVG(i.under5_mortality), 2)           AS avg_mortality,
    ROUND(MIN(i.under5_mortality), 2)           AS min_mortality,
    ROUND(MAX(i.under5_mortality), 2)           AS max_mortality,
    -- Adolescent fertility stats
    ROUND(AVG(i.adolescent_fertility), 2)       AS avg_fertility,
    ROUND(MIN(i.adolescent_fertility), 2)       AS min_fertility,
    ROUND(MAX(i.adolescent_fertility), 2)       AS max_fertility
FROM indicators i
JOIN countries c ON i.country_code = c.country_code
GROUP BY i.country_code
ORDER BY avg_life_exp DESC;

SELECT * FROM summary_stats;

-- ── 2. DECADE AVERAGES PER COUNTRY ──────────────────────────────────────────

DROP VIEW IF EXISTS decade_averages;
CREATE VIEW decade_averages AS
SELECT
    c.country_name,
    c.demographic_group,
    i.decade,
    ROUND(AVG(i.life_expectancy), 2)        AS avg_life_exp,
    ROUND(AVG(i.under5_mortality), 2)       AS avg_mortality,
    ROUND(AVG(i.adolescent_fertility), 2)   AS avg_fertility
FROM indicators i
JOIN countries c ON i.country_code = c.country_code
GROUP BY i.country_code, i.decade
ORDER BY i.country_code, i.decade;

SELECT * FROM decade_averages;

-- ── 3. IMPROVEMENT OVER TIME ─────────────────────────────────────────────────
-- Compare 1990 values vs 2022 values to measure progress

DROP VIEW IF EXISTS improvement;
CREATE VIEW improvement AS
SELECT
    c.country_name,
    c.demographic_group,
    -- Life expectancy change
    ROUND(MAX(CASE WHEN i.year = 2022 THEN i.life_expectancy END) -
          MAX(CASE WHEN i.year = 1990 THEN i.life_expectancy END), 2)
          AS life_exp_gain,
    -- Under-5 mortality change (negative = improvement)
    ROUND(MAX(CASE WHEN i.year = 2022 THEN i.under5_mortality END) -
          MAX(CASE WHEN i.year = 1990 THEN i.under5_mortality END), 2)
          AS mortality_change,
    -- Adolescent fertility change (negative = decline in births)
    ROUND(MAX(CASE WHEN i.year = 2022 THEN i.adolescent_fertility END) -
          MAX(CASE WHEN i.year = 1990 THEN i.adolescent_fertility END), 2)
          AS fertility_change,
    -- 1990 baseline values
    ROUND(MAX(CASE WHEN i.year = 1990 THEN i.life_expectancy END), 2)
          AS life_exp_1990,
    ROUND(MAX(CASE WHEN i.year = 2022 THEN i.life_expectancy END), 2)
          AS life_exp_2022,
    ROUND(MAX(CASE WHEN i.year = 1990 THEN i.under5_mortality END), 2)
          AS mortality_1990,
    ROUND(MAX(CASE WHEN i.year = 2022 THEN i.under5_mortality END), 2)
          AS mortality_2022,
    ROUND(MAX(CASE WHEN i.year = 1990 THEN i.adolescent_fertility END), 2)
          AS fertility_1990,
    ROUND(MAX(CASE WHEN i.year = 2022 THEN i.adolescent_fertility END), 2)
          AS fertility_2022
FROM indicators i
JOIN countries c ON i.country_code = c.country_code
GROUP BY i.country_code
ORDER BY life_exp_gain DESC;

SELECT * FROM improvement;

-- ── 4. VOLATILITY (GDP GROWTH PROXY) ────────────────────────────────────────
-- Standard deviation of each indicator per country
-- Higher volatility = less stable demographic trajectory

DROP VIEW IF EXISTS volatility;
CREATE VIEW volatility AS
SELECT
    c.country_name,
    c.demographic_group,
    -- Using variance approximation since SQLite has no STDEV
    ROUND(AVG((i.life_expectancy -
        (SELECT AVG(life_expectancy)
         FROM indicators
         WHERE country_code = i.country_code)) *
        (i.life_expectancy -
        (SELECT AVG(life_expectancy)
         FROM indicators
         WHERE country_code = i.country_code))), 2)
         AS life_exp_variance,
    ROUND(AVG((i.under5_mortality -
        (SELECT AVG(under5_mortality)
         FROM indicators
         WHERE country_code = i.country_code)) *
        (i.under5_mortality -
        (SELECT AVG(under5_mortality)
         FROM indicators
         WHERE country_code = i.country_code))), 2)
         AS mortality_variance,
    ROUND(AVG((i.adolescent_fertility -
        (SELECT AVG(adolescent_fertility)
         FROM indicators
         WHERE country_code = i.country_code)) *
        (i.adolescent_fertility -
        (SELECT AVG(adolescent_fertility)
         FROM indicators
         WHERE country_code = i.country_code))), 2)
         AS fertility_variance
FROM indicators i
JOIN countries c ON i.country_code = c.country_code
GROUP BY i.country_code
ORDER BY life_exp_variance DESC;

SELECT * FROM volatility;

-- ── 5. RANKINGS ──────────────────────────────────────────────────────────────
-- Rank countries by each indicator in 2022

DROP VIEW IF EXISTS rankings_2022;
CREATE VIEW rankings_2022 AS
SELECT
    c.country_name,
    c.demographic_group,
    i.life_expectancy,
    i.under5_mortality,
    i.adolescent_fertility,
    RANK() OVER (ORDER BY i.life_expectancy DESC)       AS life_exp_rank,
    RANK() OVER (ORDER BY i.under5_mortality ASC)       AS mortality_rank,
    RANK() OVER (ORDER BY i.adolescent_fertility ASC)   AS fertility_rank
FROM indicators i
JOIN countries c ON i.country_code = c.country_code
WHERE i.year = 2022
ORDER BY life_exp_rank;

SELECT * FROM rankings_2022;

-- ── 6. DEMOGRAPHIC GROUP AVERAGES ────────────────────────────────────────────
-- Average indicators by demographic group across all years

DROP VIEW IF EXISTS group_averages;
CREATE VIEW group_averages AS
SELECT
    c.demographic_group,
    i.decade,
    ROUND(AVG(i.life_expectancy), 2)        AS avg_life_exp,
    ROUND(AVG(i.under5_mortality), 2)       AS avg_mortality,
    ROUND(AVG(i.adolescent_fertility), 2)   AS avg_fertility,
    COUNT(DISTINCT i.country_code)          AS num_countries
FROM indicators i
JOIN countries c ON i.country_code = c.country_code
GROUP BY c.demographic_group, i.decade
ORDER BY c.demographic_group, i.decade;

SELECT * FROM group_averages;