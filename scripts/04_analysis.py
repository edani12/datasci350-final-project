"""
04_analysis.py
--------------
Python analysis and visualisation script for
Demographic Transitions and Healthcare Demand in East Asia
Generates all figures saved to the figures/ folder
"""

import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
import numpy as np
import os

# ── 1. SETUP ─────────────────────────────────────────────────────────────────

os.makedirs('figures', exist_ok=True)

# Colour palette by demographic group
GROUP_COLOURS = {
    'Aged Economy':    '#2C3E50',
    'Rapidly Aging':   '#E74C3C',
    'Transitioning':   '#F39C12',
    'Young Economy':   '#27AE60',
    'Benchmark':       '#8E44AD'
}

# Country to colour mapping
COUNTRY_COLOURS = {
    'Japan':          '#2C3E50',
    'South Korea':    '#E74C3C',
    'China':          '#C0392B',
    'Singapore':      '#E67E22',
    'Thailand':       '#F39C12',
    'Vietnam':        '#27AE60',
    'Indonesia':      '#1E8449',
    'United States':  '#8E44AD'
}

plt.rcParams.update({
    'figure.dpi':         200,          
    'font.family':        'sans-serif',
    'axes.labelweight':   'bold',
    'axes.titleweight':   'bold',
    'axes.titlesize':     16,
    'axes.titlepad':      20,
    'axes.grid':          True,
    'grid.alpha':         0.15,         
    'grid.linestyle':     '--',
    'legend.frameon':     False,        
    'axes.spines.top':    False,
    'axes.spines.right':  False
})

# ── 2. LOAD DATA FROM SQLITE ─────────────────────────────────────────────────

conn = sqlite3.connect('data/healthcare_demographics.db')

df = pd.read_sql('SELECT * FROM clean_data', conn)
improvement = pd.read_sql('SELECT * FROM improvement', conn)
rankings = pd.read_sql('SELECT * FROM rankings_2022', conn)
decade_avg = pd.read_sql('SELECT * FROM decade_averages', conn)
group_avg = pd.read_sql('SELECT * FROM group_averages', conn)
summary = pd.read_sql('SELECT * FROM summary_stats', conn)

conn.close()

print(f'Loaded {len(df)} rows from clean_data view')
print(f'Countries: {df["country_name"].unique()}')

# ── 3. FIGURE 1: LIFE EXPECTANCY OVER TIME ───────────────────────────────────

fig, ax = plt.subplots(figsize=(12, 7))

for country, group in df.groupby('country_name'):
    colour = COUNTRY_COLOURS.get(country, 'grey')
    
    ax.fill_between(group['year'], group['life_expectancy'], alpha=0.03, color=colour)
    
    ax.plot(
        group['year'],
        group['life_expectancy'],
        label=country,
        color=colour,
        linewidth=3,
        alpha=0.9
    )
    last = group.sort_values('year').iloc[-1]
    ax.annotate(
        country,
        xy=(last['year'], last['life_expectancy']),
        xytext=(3, 0),
        textcoords='offset points',
        fontsize=8,
        color=colour
    )

ax.set_title('Life Expectancy at Birth (1990–2022)\nEast Asia & Benchmark',
             fontsize=14, fontweight='bold', pad=15)
ax.set_xlabel('Year', fontsize=11)
ax.set_ylabel('Life Expectancy (years)', fontsize=11)
ax.set_xlim(1990, 2025)
ax.set_ylim(60, 90)
ax.legend(bbox_to_anchor=(1.01, 1), loc='upper left', fontsize=9)
ax.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('figures/01_life_expectancy.png', bbox_inches='tight')
plt.close()
print('Saved figures/01_life_expectancy.png')

# ── 4. FIGURE 2: UNDER-5 MORTALITY OVER TIME ─────────────────────────────────

fig, ax = plt.subplots(figsize=(12, 7))

for country, group in df.groupby('country_name'):
    colour = COUNTRY_COLOURS.get(country, 'grey')
    ax.plot(
        group['year'],
        group['under5_mortality'],
        label=country,
        color=colour,
        linewidth=2.5
    )
    last = group.sort_values('year').iloc[-1]
    ax.annotate(
        country,
        xy=(last['year'], last['under5_mortality']),
        xytext=(3, 0),
        textcoords='offset points',
        fontsize=8,
        color=colour
    )

ax.set_title('Under-5 Mortality Rate (1990–2022)\nPer 1,000 Live Births',
             fontsize=14, fontweight='bold', pad=15)
ax.set_xlabel('Year', fontsize=11)
ax.set_ylabel('Deaths per 1,000 Live Births', fontsize=11)
ax.set_xlim(1990, 2025)
ax.legend(bbox_to_anchor=(1.01, 1), loc='upper left', fontsize=9)
ax.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('figures/02_under5_mortality.png', bbox_inches='tight')
plt.close()
print('Saved figures/02_under5_mortality.png')

# ── 5. FIGURE 3: ADOLESCENT FERTILITY OVER TIME ──────────────────────────────

fig, ax = plt.subplots(figsize=(12, 7))

for country, group in df.groupby('country_name'):
    colour = COUNTRY_COLOURS.get(country, 'grey')
    ax.plot(
        group['year'],
        group['adolescent_fertility'],
        label=country,
        color=colour,
        linewidth=2.5
    )
    last = group.sort_values('year').iloc[-1]
    ax.annotate(
        country,
        xy=(last['year'], last['adolescent_fertility']),
        xytext=(3, 0),
        textcoords='offset points',
        fontsize=8,
        color=colour
    )

ax.set_title('Adolescent Fertility Rate (1990–2022)\nBirths per 1,000 Women Aged 15-19',
             fontsize=14, fontweight='bold', pad=15)
ax.set_xlabel('Year', fontsize=11)
ax.set_ylabel('Births per 1,000 Women (15-19)', fontsize=11)
ax.set_xlim(1990, 2025)
ax.legend(bbox_to_anchor=(1.01, 1), loc='upper left', fontsize=9)
ax.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('figures/03_adolescent_fertility.png', bbox_inches='tight')
plt.close()
print('Saved figures/03_adolescent_fertility.png')

# ── 6. FIGURE 4: IMPROVEMENT BAR CHARTS ─────────────────────────────────────

fig, axes = plt.subplots(1, 3, figsize=(16, 6))

# Life expectancy gain
colours = [GROUP_COLOURS[g] for g in improvement['demographic_group']]
axes[0].barh(improvement['country_name'],
             improvement['life_exp_gain'],
             color=colours)
axes[0].set_title('Life Expectancy\nGain (years)', fontweight='bold')
axes[0].set_xlabel('Years gained 1990-2022')
axes[0].axvline(0, color='black', linewidth=0.8)

# Mortality reduction
axes[1].barh(improvement['country_name'],
             improvement['mortality_change'].abs(),
             color=colours)
axes[1].set_title('Under-5 Mortality\nReduction', fontweight='bold')
axes[1].set_xlabel('Deaths reduced per 1,000 (1990-2022)')

# Fertility decline
axes[2].barh(improvement['country_name'],
             improvement['fertility_change'].abs(),
             color=colours)
axes[2].set_title('Adolescent Fertility\nDecline', fontweight='bold')
axes[2].set_xlabel('Births reduced per 1,000 (1990-2022)')

# Add legend
from matplotlib.patches import Patch
legend_elements = [Patch(facecolor=c, label=g)
                   for g, c in GROUP_COLOURS.items()]
fig.legend(handles=legend_elements,
           loc='lower center',
           ncol=5,
           fontsize=9,
           bbox_to_anchor=(0.5, -0.05))

plt.suptitle('Demographic Improvement by Country (1990–2022)',
             fontsize=14, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig('figures/04_improvement.png', bbox_inches='tight')
plt.close()
print('Saved figures/04_improvement.png')

# ── 7. FIGURE 5: 2022 RANKINGS HEATMAP ───────────────────────────────────────

fig, ax = plt.subplots(figsize=(10, 6))

# Normalise indicators to 0-1 scale for heatmap
heatmap_data = rankings[['country_name',
                          'life_expectancy',
                          'under5_mortality',
                          'adolescent_fertility']].copy()
heatmap_data = heatmap_data.set_index('country_name')

# Normalise each column
for col in heatmap_data.columns:
    heatmap_data[col] = (heatmap_data[col] - heatmap_data[col].min()) / \
                        (heatmap_data[col].max() - heatmap_data[col].min())

# Invert mortality and fertility so higher = better for all
heatmap_data['under5_mortality'] = 1 - heatmap_data['under5_mortality']
heatmap_data['adolescent_fertility'] = 1 - heatmap_data['adolescent_fertility']

heatmap_data.columns = ['Life Expectancy', 'Child Survival', 'Low Teen Fertility']

sns.heatmap(
    heatmap_data,
    annot=True,
    fmt='.2f',
    cmap='YlGnBu',
    linewidths=2,
    cbar=False,
    square=True,
    ax=ax,
    annot_kws={"size": 10, "weight": "bold"} # Clearer labels
)

ax.set_title('Demographic Health Scorecard (2022)\nNormalised 0-1 Scale',
             fontsize=14, fontweight='bold', pad=15)
ax.set_ylabel('')

plt.tight_layout()
plt.savefig('figures/05_scorecard_heatmap.png', bbox_inches='tight')
plt.close()
print('Saved figures/05_scorecard_heatmap.png')

# ── 8. FIGURE 6: GROUP AVERAGES OVER DECADES ─────────────────────────────────

fig, axes = plt.subplots(1, 3, figsize=(16, 5))

indicators = ['avg_life_exp', 'avg_mortality', 'avg_fertility']
titles = ['Life Expectancy', 'Under-5 Mortality', 'Adolescent Fertility']
ylabels = ['Years', 'Per 1,000 Births', 'Per 1,000 Women (15-19)']

for ax, ind, title, ylabel in zip(axes, indicators, titles, ylabels):
    for group, gdata in group_avg.groupby('demographic_group'):
        colour = GROUP_COLOURS.get(group, 'grey')
        ax.plot(gdata['decade'], gdata[ind],
                marker='o', label=group,
                color=colour, linewidth=2.5,
                markersize=8)
    ax.set_title(title, fontweight='bold')
    ax.set_xlabel('Decade')
    ax.set_ylabel(ylabel)
    ax.grid(axis='y', alpha=0.3)

handles, labels = axes[0].get_legend_handles_labels()
fig.legend(handles, labels,
           loc='lower center',
           ncol=5,
           fontsize=9,
           bbox_to_anchor=(0.5, -0.08))

plt.suptitle('Demographic Trends by Country Group (1990s–2020s)',
             fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('figures/06_group_trends.png', bbox_inches='tight')
plt.close()
print('Saved figures/06_group_trends.png')

# ── 9. FIGURE 7: SCATTER - LIFE EXP vs MORTALITY 2022 ────────────────────────

fig, ax = plt.subplots(figsize=(10, 7))

data_2022 = df[df['year'] == 2022].copy()

for _, row in data_2022.iterrows():
    colour = GROUP_COLOURS.get(row['demographic_group'], 'grey')
    ax.scatter(
        row['under5_mortality'],
        row['life_expectancy'],
        color=colour,
        s=300,
        edgecolor='white',
        linewidth=1.5,
        alpha=0.85,
        zorder=5
    )
    ax.annotate(
        row['country_name'],
        xy=(row['under5_mortality'], row['life_expectancy']),
        xytext=(5, 5),
        textcoords='offset points',
        fontsize=9
    )

# Add trend line
x = data_2022['under5_mortality']
y = data_2022['life_expectancy']
z = np.polyfit(x, y, 1)
p = np.poly1d(z)
x_line = np.linspace(x.min(), x.max(), 100)
ax.plot(x_line, p(x_line), '--', color='grey',
        alpha=0.7, linewidth=1.5, label='Trend')

ax.set_title('Life Expectancy vs Under-5 Mortality (2022)\nEast Asia & Benchmark',
             fontsize=14, fontweight='bold', pad=15)
ax.set_xlabel('Under-5 Mortality Rate (per 1,000 births)', fontsize=11)
ax.set_ylabel('Life Expectancy (years)', fontsize=11)
ax.grid(alpha=0.3)

legend_elements = [Patch(facecolor=c, label=g)
                   for g, c in GROUP_COLOURS.items()]
ax.legend(handles=legend_elements, fontsize=9)

plt.tight_layout()
plt.savefig('figures/07_scatter_2022.png', bbox_inches='tight')
plt.close()
print('Saved figures/07_scatter_2022.png')

# ── 10. ADDITIONAL ANALYSIS (added by Nikhil) ─────────────────────────────

print("\n--- Additional Analysis: Fertility vs Life Expectancy ---")

# Correlation matrix
corr = df[['life_expectancy', 'under5_mortality', 'adolescent_fertility']].corr()
print("\nCorrelation Matrix:")
print(corr)

# Scatter plot: fertility vs life expectancy
fig, ax = plt.subplots(figsize=(10, 7))

for group, gdata in df.groupby('demographic_group'):
    colour = GROUP_COLOURS.get(group, 'grey')
    ax.scatter(
        gdata['adolescent_fertility'],
        gdata['life_expectancy'],
        color=colour,
        alpha=0.6,
        s=70,
        label=group
    )

ax.set_title('Adolescent Fertility vs Life Expectancy',
             fontsize=14, fontweight='bold')
ax.set_xlabel('Adolescent Fertility Rate (per 1,000 women)')
ax.set_ylabel('Life Expectancy (years)')
ax.grid(alpha=0.3)
ax.legend()

plt.tight_layout()
plt.savefig('figures/08_fertility_vs_life.png')
plt.close()

print("Saved figures/08_fertility_vs_life.png")

print('\nAll figures saved to figures/ folder.')
print('Analysis complete.')

