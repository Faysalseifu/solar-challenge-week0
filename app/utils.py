"""Utility functions for loading, summarizing and plotting solar data."""
from pathlib import Path
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
import os


sns.set(style="whitegrid")


def find_data_root():
    """Search parent directories for a `Data` folder and return its Path.

    Falls back to ./Data if not found in parents.
    """
    curr = Path.cwd().resolve()
    for parent in [curr] + list(curr.parents):
        if (parent / "Data").is_dir():
            return parent / "Data"
    return Path("./Data").resolve()


def discover_clean_files(data_root: Path = None):
    data_root = data_root or find_data_root()
    return list(Path(data_root).glob("*_clean.csv"))


def load_clean_files(files):
    dfs = {}
    for p in files:
        df = pd.read_csv(p)
        country = p.name.split("_clean")[0] or p.stem
        df["country"] = country
        dfs[country] = df
    return dfs


def merge_dataframes(dfs: dict):
    if not dfs:
        return pd.DataFrame()
    merged = pd.concat(dfs.values(), ignore_index=True, sort=False)
    return merged


def summary_table(df: pd.DataFrame, metrics=None):
    metrics = metrics or ["GHI", "DNI", "DHI"]
    present = [m for m in metrics if m in df.columns]
    if not present:
        return pd.DataFrame()
    summary = df.groupby("country")[present].agg(["mean", "median", "std"]).round(3)
    summary.columns = ["_".join(col).strip() for col in summary.columns.values]
    return summary.reset_index()


def create_plots(merged: pd.DataFrame, out_dir: Path, metrics=None):
    metrics = metrics or ["GHI", "DNI", "DHI"]
    out_dir.mkdir(exist_ok=True)
    saved = []
    for metric in metrics:
        if metric not in merged.columns:
            continue
        plt.figure(figsize=(8, 4))
        sns.boxplot(x="country", y=metric, data=merged, palette="Set2")
        plt.title(f"Boxplot of {metric} by country")
        plt.tight_layout()
        fp = out_dir / f"boxplot_{metric}.png"
        plt.savefig(fp, dpi=150)
        plt.close()
        saved.append(fp)

    if "GHI" in merged.columns:
        avg = merged.groupby("country")["GHI"].mean().sort_values(ascending=False)
        plt.figure(figsize=(6, 3))
        sns.barplot(x=avg.values, y=avg.index, palette="viridis")
        plt.xlabel("Average GHI")
        plt.title("Countries ranked by average GHI")
        plt.tight_layout()
        fp = out_dir / "rank_by_avg_GHI.png"
        plt.savefig(fp, dpi=150)
        plt.close()
        saved.append(fp)

    return saved


def generate_outputs(data_root: Path = None, out_dir: Path = Path("outputs")):
    """Discover cleaned CSVs, create a merged dataframe, summary CSV and plots.

    Returns (summary_dataframe, list_of_image_paths)
    """
    data_root = Path(data_root) if data_root else None
    files = discover_clean_files(data_root)
    if not files:
        raise RuntimeError("No *_clean.csv files found in Data/ to process.")
    dfs = load_clean_files(files)
    merged = merge_dataframes(dfs)
    summary = summary_table(merged)
    out_dir = Path(out_dir)
    out_dir.mkdir(exist_ok=True)
    if not summary.empty:
        summary.to_csv(out_dir / "summary_stats.csv", index=False)
    images = create_plots(merged, out_dir)
    return summary, images


def read_summary(out_dir: Path = Path("outputs")):
    p = Path(out_dir) / "summary_stats.csv"
    if not p.exists():
        raise FileNotFoundError(p)
    return pd.read_csv(p)
