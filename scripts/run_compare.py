"""scripts/run_compare.py

Quick runner to perform cross-country comparison for Ethiopia and Canada.
Saves summary table and plots to outputs/.

Usage:
    python scripts/run_compare.py

The script looks for Data/ethiopia_clean.csv and Data/canada_clean.csv in the repository root (walks parent directories).
"""
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import os

sns.set(style='whitegrid')


def find_data_root():
    curr = Path.cwd().resolve()
    for parent in [curr] + list(curr.parents):
        if (parent / 'Data').is_dir():
            return parent / 'Data'
    return curr / 'Data'


def load_country(path: Path):
    if not path.exists():
        print(f"Missing file: {path}")
        return None
    try:
        df = pd.read_csv(path)
        return df
    except Exception as e:
        print(f"Failed to load {path}: {e}")
        return None


def ensure_outputs():
    out = Path('outputs')
    out.mkdir(exist_ok=True)
    return out


def summary_table(merged, metrics=['GHI','DNI','DHI']):
    present = [m for m in metrics if m in merged.columns]
    if len(present) == 0:
        return pd.DataFrame()
    summary = merged.groupby('country')[present].agg(['mean','median','std']).round(3)
    summary.columns = ['_'.join(col).strip() for col in summary.columns.values]
    return summary.reset_index()


def plot_boxplots(merged, metrics, outdir: Path):
    for metric in metrics:
        if metric not in merged.columns:
            print(f"Skipping boxplot for missing metric: {metric}")
            continue
        fig, ax = plt.subplots(figsize=(8,4))
        sns.boxplot(x='country', y=metric, data=merged, palette='Set2', ax=ax)
        ax.set_title(f'Boxplot of {metric} by country')
        plt.tight_layout()
        out_path = outdir / f'boxplot_{metric}.png'
        fig.savefig(out_path, dpi=150)
        plt.close(fig)
        print('Saved', out_path)


def plot_bar_ranking(merged, outdir: Path):
    if 'GHI' not in merged.columns:
        print('No GHI column for ranking')
        return
    avg = merged.groupby('country')['GHI'].mean().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(6,4))
    sns.barplot(x=avg.values, y=avg.index, palette='viridis', ax=ax)
    ax.set_xlabel('Average GHI')
    ax.set_title('Countries ranked by average GHI')
    plt.tight_layout()
    out_path = outdir / 'rank_by_avg_GHI.png'
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
    print('Saved', out_path)


def run_stat_tests(merged):
    if 'GHI' not in merged.columns:
        print('No GHI column for statistical tests')
        return None
    groups = [group.dropna() for _, group in merged.groupby('country')['GHI']]
    groups = [g for g in groups if len(g) > 0]
    if len(groups) < 2:
        print('Not enough groups/data for statistical testing')
        return None
    results = {}
    try:
        f_stat, p_anova = stats.f_oneway(*groups)
        results['anova'] = (f_stat, p_anova)
    except Exception as e:
        results['anova'] = ('failed', str(e))
    try:
        h_stat, p_kruskal = stats.kruskal(*groups)
        results['kruskal'] = (h_stat, p_kruskal)
    except Exception as e:
        results['kruskal'] = ('failed', str(e))
    return results


def main():
    data_root = find_data_root()
    print('Using Data root:', data_root)

    # expected files
    files = {
        'ethiopia': data_root / 'ethiopia_clean.csv',
        'canada': data_root / 'canada_clean.csv'
    }

    dfs = {}
    for name, path in files.items():
        df = load_country(path)
        if df is not None:
            df['country'] = name
            dfs[name] = df
            print('Loaded', name, df.shape)

    if len(dfs) == 0:
        print('No data loaded. Exiting.')
        return

    merged = pd.concat(dfs.values(), ignore_index=True, sort=False)
    print('Merged shape:', merged.shape)

    outdir = ensure_outputs()

    # Summary
    summary = summary_table(merged)
    if not summary.empty:
        summary_path = outdir / 'summary_stats.csv'
        summary.to_csv(summary_path, index=False)
        print('Saved summary to', summary_path)
        print(summary)
    else:
        print('No summary (missing metrics)')

    # Plots
    plot_boxplots(merged, ['GHI','DNI','DHI'], outdir)
    plot_bar_ranking(merged, outdir)

    # Stats
    results = run_stat_tests(merged)
    if results is not None:
        print('\nStatistical test results:')
        for k,v in results.items():
            print(k, ':', v)
        # write to file
        with open(outdir / 'stat_tests.txt','w') as f:
            for k,v in results.items():
                f.write(f"{k}: {v}\n")

    print('\nDone. Outputs saved to', outdir)


if __name__ == '__main__':
    main()
