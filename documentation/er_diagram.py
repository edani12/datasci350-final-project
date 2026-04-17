"""
er_diagram.py
-------------
Generates an Entity-Relationship diagram for the
healthcare demographics SQLite database
Saves to documentation/er_diagram.png
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import os

fig, ax = plt.subplots(1, 1, figsize=(14, 10))
ax.set_xlim(0, 14)
ax.set_ylim(0, 10)
ax.axis('off')

# ── TITLE ─────────────────────────────────────────────────────────────────────

ax.text(7, 9.5, 'Entity-Relationship Diagram',
        ha='center', va='center',
        fontsize=16, fontweight='bold')
ax.text(7, 9.1, 'Demographic Transitions and Healthcare Demand in East Asia',
        ha='center', va='center',
        fontsize=11, color='grey')

# ── HELPER FUNCTIONS ──────────────────────────────────────────────────────────

def draw_table(ax, x, y, width, height, title, columns, pk_cols=None, fk_cols=None):
    """Draw a database table box with columns listed inside."""
    # Table border
    rect = FancyBboxPatch(
        (x, y), width, height,
        boxstyle='round,pad=0.05',
        linewidth=2,
        edgecolor='#2C3E50',
        facecolor='#EBF5FB'
    )
    ax.add_patch(rect)

    # Title bar
    title_rect = FancyBboxPatch(
        (x, y + height - 0.45), width, 0.45,
        boxstyle='round,pad=0.02',
        linewidth=0,
        edgecolor='#2C3E50',
        facecolor='#2C3E50'
    )
    ax.add_patch(title_rect)

    # Table name
    ax.text(x + width/2, y + height - 0.22,
            title, ha='center', va='center',
            fontsize=11, fontweight='bold',
            color='white')

    # Columns
    row_height = (height - 0.5) / len(columns)
    for i, col in enumerate(columns):
        row_y = y + height - 0.5 - (i + 0.5) * row_height

        # Highlight PK in gold, FK in orange
        if pk_cols and col.split()[0] in pk_cols:
            color = '#F39C12'
            prefix = '🔑 '
        elif fk_cols and col.split()[0] in fk_cols:
            color = '#E74C3C'
            prefix = '🔗 '
        else:
            color = '#2C3E50'
            prefix = '    '

        ax.text(x + 0.15, row_y,
                prefix + col,
                ha='left', va='center',
                fontsize=8.5, color=color)

        # Row divider
        if i < len(columns) - 1:
            ax.plot([x, x + width],
                    [y + height - 0.5 - (i+1)*row_height,
                     y + height - 0.5 - (i+1)*row_height],
                    color='#BDC3C7', linewidth=0.5)

def draw_arrow(ax, x1, y1, x2, y2, label=''):
    """Draw a relationship arrow between tables."""
    ax.annotate('',
                xy=(x2, y2),
                xytext=(x1, y1),
                arrowprops=dict(
                    arrowstyle='-|>',
                    color='#7F8C8D',
                    lw=2,
                    connectionstyle='arc3,rad=0.0'
                ))
    if label:
        mid_x = (x1 + x2) / 2
        mid_y = (y1 + y2) / 2
        ax.text(mid_x, mid_y + 0.15, label,
                ha='center', va='center',
                fontsize=8, color='#7F8C8D',
                style='italic')

# ── DRAW COUNTRIES TABLE ──────────────────────────────────────────────────────

countries_cols = [
    'country_code    TEXT',
    'country_name    TEXT',
    'demographic_group TEXT'
]

draw_table(
    ax, x=1, y=5.5,
    width=4, height=2.2,
    title='countries',
    columns=countries_cols,
    pk_cols=['country_code']
)

# ── DRAW INDICATORS TABLE ─────────────────────────────────────────────────────

indicators_cols = [
    'id                    INTEGER',
    'country_code          TEXT',
    'year                  INTEGER',
    'life_expectancy       REAL',
    'under5_mortality      REAL',
    'adolescent_fertility  REAL',
    'decade                TEXT'
]

draw_table(
    ax, x=7.5, y=4.2,
    width=5.5, height=3.8,
    title='indicators',
    columns=indicators_cols,
    pk_cols=['id'],
    fk_cols=['country_code']
)

# ── DRAW COMBINED_INDICATORS TABLE ────────────────────────────────────────────

combined_cols = [
    'country_code          TEXT',
    'country_name          TEXT',
    'year                  INTEGER',
    'life_expectancy       REAL',
    'under5_mortality      REAL',
    'adolescent_fertility  REAL',
    'demographic_group     TEXT',
    'decade                TEXT'
]

draw_table(
    ax, x=1, y=0.5,
    width=5, height=3.8,
    title='combined_indicators (raw)',
    columns=combined_cols,
    pk_cols=[],
    fk_cols=[]
)

# ── DRAW ARROWS ───────────────────────────────────────────────────────────────

# countries -> indicators (one to many)
draw_arrow(ax, 5, 6.5, 7.5, 6.5, '1 : many')

# combined_indicators -> indicators (source)
draw_arrow(ax, 6, 3.5, 7.5, 5.2, 'source for')

# ── DRAW VIEWS BOX ────────────────────────────────────────────────────────────

views_rect = FancyBboxPatch(
    (1, 8.2), 12, 0.7,
    boxstyle='round,pad=0.05',
    linewidth=1.5,
    edgecolor='#27AE60',
    facecolor='#EAFAF1'
)
ax.add_patch(views_rect)

ax.text(7, 8.75, 'VIEWS (derived from indicators + countries)',
        ha='center', va='center',
        fontsize=9, fontweight='bold', color='#27AE60')

views = ['clean_data', 'summary_stats', 'decade_averages',
         'improvement', 'volatility', 'rankings_2022', 'group_averages']
for i, view in enumerate(views):
    ax.text(1.5 + i * 1.72, 8.38, view,
            ha='center', va='center',
            fontsize=7.5, color='#27AE60',
            style='italic')

# Arrow from tables to views
draw_arrow(ax, 7, 7.7, 7, 8.2, '')

# ── LEGEND ────────────────────────────────────────────────────────────────────

legend_elements = [
    mpatches.Patch(facecolor='#F39C12', label='Primary Key (PK)'),
    mpatches.Patch(facecolor='#E74C3C', label='Foreign Key (FK)'),
    mpatches.Patch(facecolor='#EBF5FB', edgecolor='#2C3E50',
                   label='Table'),
    mpatches.Patch(facecolor='#EAFAF1', edgecolor='#27AE60',
                   label='View')
]
ax.legend(handles=legend_elements,
          loc='lower right',
          fontsize=9,
          framealpha=0.9)

plt.tight_layout()
plt.savefig('documentation/er_diagram.png',
            bbox_inches='tight', dpi=150)
plt.close()
print('Saved documentation/er_diagram.png')