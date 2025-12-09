"""
Script to export Plotly plots from the notebook as HTML files for the website.
Run this script after running the relevant cells in final-proj-submission.ipynb
"""

import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from scipy.stats import gaussian_kde
from pathlib import Path

# Create plots directory if it doesn't exist
plots_dir = Path("assets/plots")
plots_dir.mkdir(parents=True, exist_ok=True)

# Load the data (you may need to adjust this path)
df = pd.read_excel('outage.xlsx')
df.columns = df.iloc[4]
df = df.iloc[6:]

# Clean data as in notebook
df = df.dropna(subset=['OUTAGE.START.DATE', 'OUTAGE.START.TIME', 'OUTAGE.RESTORATION.TIME'])
df['OUTAGE.START'] = pd.to_datetime(df['OUTAGE.START.DATE'].astype(str) + " " + df['OUTAGE.START.TIME'].astype(str), errors='coerce')
df['OUTAGE.RESTORATION'] = pd.to_datetime(df['OUTAGE.RESTORATION.DATE'].astype(str) + " " + df['OUTAGE.RESTORATION.TIME'].astype(str), errors='coerce')
df['is_intentional'] = (df['CAUSE.CATEGORY'] == 'intentional attack')
df['aa_gsp'] = (df['PC.REALGSP.REL'] > 1)

# Plot 1: KDE for electricity prices
print("Creating KDE plot for electricity prices...")
features = ['RES.PRICE', 'COM.PRICE', 'IND.PRICE']
fig = go.Figure()

for f in features:
    vals = pd.to_numeric(df[f], errors="coerce").dropna()
    if vals.empty:
        print(f"Skipping non-numeric or empty column: {f}")
        continue
    
    try:
        kde = gaussian_kde(vals)
        x_range = np.linspace(vals.min(), vals.max(), 300)
        y_vals = kde(x_range)
        fig.add_trace(
            go.Scatter(
                x=x_range,
                y=y_vals,
                mode='lines',
                name=f
            )
        )
    except Exception as e:
        print(f"Skipping {f} due to error: {e}")
        continue

fig.update_layout(
    title="KDE Plot for Monthly Electricity Prices in Different Sectors",
    xaxis_title="Monthly Electricity Price",
    yaxis_title="Density",
    legend_title="Region",
    width=900,
    height=500
)

fig.write_html(str(plots_dir / "kde_prices.html"))
print(f"✓ Saved to {plots_dir / 'kde_prices.html'}")

# Plot 2: Scatter plot of GSP vs Commercial Consumption
print("Creating scatter plot for GSP vs Commercial Consumption...")
fig2 = px.scatter(df, x='PC.REALGSP.REL', y='COM.PERCEN', color='CAUSE.CATEGORY', 
                 title='Relative State GSP vs. Commercial Electricity Consumption',
                 width=900, 
                 height=600)

fig2.write_html(str(plots_dir / "scatter_gsp_com.html"))
print(f"✓ Saved to {plots_dir / 'scatter_gsp_com.html'}")

print("\nAll plots exported successfully!")

