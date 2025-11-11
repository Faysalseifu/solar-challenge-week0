Cross-country comparison helper scripts

Place cleaned CSVs in Data/ with names like `benin_clean.csv`, `sierraleone_clean.csv`, `togo_clean.csv`.

To run the Streamlit app locally:

```bash
pip install -r requirments.txt
streamlit run app/main.py
```

Notes:
- The app reads local CSVs from the `Data/` directory. Keep `Data/` in `.gitignore`.
- `app/utils.py` contains helper functions to load country CSVs and compute summary tables.
