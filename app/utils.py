import os
import pandas as pd

def load_countries():
    """Return dict of available cleaned country DataFrames found in Data/"""
    data_dir = os.path.join(os.getcwd(), 'Data')
    result = {}
    if not os.path.isdir(data_dir):
        return result
    for filepath in os.listdir(data_dir):
        if filepath.endswith('_clean.csv'):
            country = filepath.replace('_clean.csv', '').capitalize()
            try:
                df = pd.read_csv(os.path.join(data_dir, filepath))
                df['country'] = country
                result[country] = df
            except Exception:
                continue
    return result

def summary_table(df):
    metrics = ['GHI','DNI','DHI']
    present = [m for m in metrics if m in df.columns]
    if len(present) == 0:
        return pd.DataFrame()
    summary = df.groupby('country')[present].agg(['mean','median','std']).round(3)
    summary.columns = ['_'.join(col).strip() for col in summary.columns.values]
    return summary.reset_index()
