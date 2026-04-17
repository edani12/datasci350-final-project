import wbgapi as wb
import pandas as pd
import sqlite3
import os

COUNTRIES = {
    'JPN': 'Japan',
    'KOR': 'South Korea',
    'CHN': 'China',
    'SGP': 'Singapore',
    'THA': 'Thailand',
    'VNM': 'Vietnam',
    'IDN': 'Indonesia',
    'USA': 'United States'
}

INDICATORS = {
    'SP.DYN.LE00.IN': 'life_expectancy',
    'SH.DYN.MORT':    'under5_mortality',
    'SP.ADO.TFRT':    'adolescent_fertility'
}

YEARS = range(1990, 2023)
DB_PATH = 'data/healthcare_demographics.db'

os.makedirs('data', exist_ok=True)

def download_indicator(indicator_code, indicator_name):
    print(f'Downloading {indicator_name} ({indicator_code})...')
    raw = wb.data.DataFrame(
        indicator_code,
        list(COUNTRIES.keys()),
        YEARS,
        numericTimeKeys=True
    )
    raw = raw.reset_index()
    raw = raw.rename(columns={'economy': 'country_code'})
    df_long = raw.melt(
        id_vars='country_code',
        var_name='year',
        value_name=indicator_name
    )
    df_long['country_name'] = df_long['country_code'].map(COUNTRIES)
    df_long['year'] = df_long['year'].astype(int)
    df_long[indicator_name] = pd.to_numeric(df_long[indicator_name], errors='coerce')
    df_long = df_long.sort_values(['country_code', 'year']).reset_index(drop=True)
    print(f'  -> {len(df_long)} rows, {df_long[indicator_name].notna().sum()} non-null values')
    return df_long

dfs = {}
for code, name in INDICATORS.items():
    dfs[name] = download_indicator(code, name)

for name, df in dfs.items():
    path = f'data/{name}.csv'
    df.to_csv(path, index=False)
    print(f'Saved {path}')

print('\nMerging indicators into combined dataset...')
combined = dfs['life_expectancy'][['country_code', 'country_name', 'year', 'life_expectancy']]
for name in ['under5_mortality', 'adolescent_fertility']:
    combined = combined.merge(
        dfs[name][['country_code', 'year', name]],
        on=['country_code', 'year'],
        how='left'
    )

COUNTRY_GROUPS = {
    'JPN': 'Aged Economy',
    'KOR': 'Rapidly Aging',
    'CHN': 'Rapidly Aging',
    'SGP': 'Rapidly Aging',
    'THA': 'Transitioning',
    'VNM': 'Transitioning',
    'IDN': 'Young Economy',
    'USA': 'Benchmark'
}

combined['demographic_group'] = combined['country_code'].map(COUNTRY_GROUPS)
combined['decade'] = (combined['year'] // 10 * 10).astype(str) + 's'

print(f'Combined dataset: {combined.shape[0]} rows x {combined.shape[1]} columns')
print(f'Missing values:\n{combined.isnull().sum()}')

combined.to_csv('data/combined_indicators.csv', index=False)
print('\nSaved data/combined_indicators.csv')

print(f'\nLoading into SQLite database: {DB_PATH}')
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

for name, df in dfs.items():
    df.to_sql(name, conn, if_exists='replace', index=False)
    print(f'  -> Loaded table: {name} ({len(df)} rows)')

combined.to_sql('combined_indicators', conn, if_exists='replace', index=False)
print(f'  -> Loaded table: combined_indicators ({len(combined)} rows)')

print('\nTables in database:')
tables = cursor.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
for t in tables:
    count = cursor.execute(f"SELECT COUNT(*) FROM {t[0]}").fetchone()[0]
    print(f'  {t[0]}: {count} rows')

conn.close()
print('\nData download complete.')
