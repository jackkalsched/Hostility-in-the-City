# Website Setup Checklist

## Before Publishing

1. **Export Plotly Plots**
   - Run `python export_plots.py` after executing the relevant cells in your notebook
   - OR manually export plots from Jupyter:
     - `kde_prices.html` → `assets/plots/kde_prices.html`
     - `scatter_gsp_com.html` → `assets/plots/scatter_gsp_com.html`

2. **Update Aggregate Table**
   - In `index.md`, find the "Interesting Aggregates" section
   - Replace the placeholder values in the climate region table with actual values from your notebook
   - The values come from: `df.groupby(['CLIMATE.REGION'])['OUTAGE.DURATION'].agg(['mean', 'std', 'count'])`

3. **Verify Configuration**
   - Check `_config.yml` - update the `url` field if your GitHub username is different
   - The `baseurl` should match your repository name: `/Hostility-in-the-City`

4. **Test Locally** (Optional but Recommended)
   ```bash
   bundle install
   bundle exec jekyll serve
   ```
   - Visit `http://localhost:4000/Hostility-in-the-City/` to preview
   - Check that all plots load correctly
   - Verify all sections are complete

5. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Add Jekyll website for GitHub Pages"
   git push
   ```

6. **Enable GitHub Pages**
   - Go to repository Settings → Pages
   - Source: Deploy from a branch
   - Branch: `main` (or your default branch)
   - Folder: `/ (root)`
   - Click Save

7. **Wait for Deployment**
   - GitHub will build your site (usually takes 1-2 minutes)
   - Your site will be available at: `https://jackkalsched.github.io/Hostility-in-the-City/`

## File Structure Created

```
Hostility-in-the-City/
├── _config.yml              # Jekyll configuration
├── _layouts/
│   └── default.html         # HTML layout template
├── assets/
│   ├── css/
│   │   └── main.css         # Custom styling
│   └── plots/               # Plotly HTML files go here
│       └── README.md
├── index.md                 # Main website content
├── Gemfile                  # Ruby dependencies
├── export_plots.py          # Script to export plots
├── README.md                # Updated with instructions
└── SETUP.md                 # This file
```

## Notes

- The website content follows all requirements from the project instructions
- All sections (Steps 1-8) are included with appropriate detail
- The site uses a modern, responsive design
- Plotly plots are embedded as iframes (make sure to export them!)
- Jekyll will automatically process Markdown and generate the HTML site

