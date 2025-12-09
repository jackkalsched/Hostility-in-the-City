# Hostility in the City

**Authors**: Jack Kalsched, Roxy Behjat

This is our final DSC80 project for the Fall '25 term.

## Project Website

The project website is available at: [GitHub Pages URL - update this after publishing]

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

## Publishing to GitHub Pages

1. Push all files to your GitHub repository

2. Go to your repository settings on GitHub

3. Navigate to "Pages" in the left sidebar

4. Under "Source", select "Deploy from a branch"

5. Choose the branch (usually `main`) and folder (`/ (root)`)

6. Click "Save"

7. GitHub Pages will automatically build and deploy your site using Jekyll

8. Your site will be available at: `https://[username].github.io/Hostility-in-the-City/`

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
