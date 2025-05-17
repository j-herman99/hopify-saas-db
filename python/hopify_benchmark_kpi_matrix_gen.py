import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import os

# Load data
df = pd.read_csv('benchmarks/hopify_kpi_benchmarks.csv')

# Pivot to create matrix
pivot = df.pivot_table(index='metric_category',
                       columns='segment',
                       values='metric_name',
                       aggfunc='count',
                       fill_value=0)

# Custom light blue to purple colormap (no white)
custom_cmap = mcolors.LinearSegmentedColormap.from_list(
    "BluePurpleGradient", ["#CFE8FF", "#5E9BD4", "#7E57C2"]
)

# Plot setup
sns.set_theme(style="white")
plt.figure(figsize=(10, 6), facecolor='#F5F5F5')

# Draw heatmap
ax = sns.heatmap(pivot,
                 annot=True,
                 fmt='d',
                 cmap=custom_cmap,
                 linewidths=0.6,
                 linecolor='#F5F5F5',
                 cbar_kws={'label': 'KPI Count'},
                 square=True)

# Labels and title
plt.title('Benchmark KPI Matrix\nby Segment and Metric Category', fontsize=16, pad=20)
plt.xlabel('Customer Segment', fontsize=12, labelpad=12)
plt.ylabel('Metric Category', fontsize=12, labelpad=12)
plt.xticks(rotation=0, fontsize=10)
plt.yticks(rotation=0, fontsize=10)

# Match figure facecolor
ax.set_facecolor('#F5F5F5')
plt.gcf().patch.set_facecolor('#F5F5F5')

# Save
os.makedirs('visuals', exist_ok=True)
plt.tight_layout(pad=2.5)
plt.savefig('visuals/hopify_benchmark_kpi_matrix.png', dpi=300, facecolor='#F5F5F5')

print("✅ Benchmark matrix with custom blue → purple gradient saved.")