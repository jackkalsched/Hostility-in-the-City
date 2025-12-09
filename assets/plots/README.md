# Plot Files

This directory should contain HTML files exported from Plotly plots in your notebook.

## Required Plots

1. **kde_prices.html** - KDE plot for monthly electricity prices in different sectors (from univariate analysis)
2. **scatter_gsp_com.html** - Scatter plot of Relative State GSP vs. Commercial Electricity Consumption (from bivariate analysis)

## How to Export Plots

In your Jupyter notebook, after creating a Plotly figure, use:

```python
fig.write_html("assets/plots/kde_prices.html")
fig.write_html("assets/plots/scatter_gsp_com.html")
```

Or use the Plotly menu: Click on the plot → Download plot as HTML

## Note

If you don't have these files yet, the website will still work, but the iframes will show empty spaces. Make sure to export your plots and place them in this directory before publishing.

