# scripts

This folder contains helper scripts for running comparisons and batch jobs.

Usage
-----
- Use `python -m scripts.run_compare` or run the Jupyter notebooks in `notebooks/` to regenerate `outputs/summary_stats.csv` and plots.
- The Streamlit app in `app/main.py` will display any files in `outputs/` (summary CSV and PNG images).

Notes
-----
- Place cleaned CSV files named like `country_clean.csv` inside the repository `Data/` directory. The utilities will search parent directories for a `Data/` folder.
