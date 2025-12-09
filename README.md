# Hostility in the City

**Authors**: Jack Kalsched, Roxana Behjat

This is our final DSC80 project for the Fall '25 term.

## Project Website

The project website is available at: www.jackkalsched.github.io/hostility-in-the-city/

## Local Development

To preview the website locally with Jekyll:

1. Install Jekyll and Bundler (if not already installed):
   ```bash
   gem install bundler jekyll
   ```

2. Install dependencies:
   ```bash
   bundle install
   ```

3. Run the Jekyll server:
   ```bash
   bundle exec jekyll serve
   ```

4. Open your browser to `http://localhost:4000`

## Exporting Plots

Before publishing, you need to export Plotly plots as HTML files:

1. Run the export script (after running your notebook):
   ```bash
   python export_plots.py
   ```

   Or manually export plots from your notebook:
   - In Jupyter, after creating a Plotly figure, use `fig.write_html("assets/plots/plot_name.html")`
   - Or use the Plotly menu: Click on the plot → Download plot as HTML

2. Place the HTML files in the `assets/plots/` directory:
   - `kde_prices.html` - KDE plot for electricity prices
   - `scatter_gsp_com.html` - Scatter plot of GSP vs Commercial Consumption

## Project Structure

```
Hostility-in-the-City/
├── _config.yml          # Jekyll configuration
├── _layouts/            # HTML layouts
│   └── default.html
├── assets/
│   ├── css/
│   │   └── main.css     # Custom styling
│   └── plots/           # Plotly HTML files (export these)
├── index.md             # Main website content
├── final-proj-submission.ipynb  # Original notebook
└── README.md            # This file
```

## Notes

- The website content is in `index.md`
- Make sure to export all Plotly plots before publishing
- Jekyll will automatically process Markdown files
- The `_config.yml` excludes notebook files and other unnecessary files from the site
