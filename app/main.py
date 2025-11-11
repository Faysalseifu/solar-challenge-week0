"""Streamlit main app for comparing solar data across countries."""
from pathlib import Path
import streamlit as st
from app import utils


st.set_page_config(page_title="Solar comparison", layout="wide")

st.title("Cross-country solar metrics comparison")

out_dir = Path("outputs")

st.sidebar.header("Data / options")
if st.sidebar.button("Reload and (re)generate outputs"):
    # force re-generate from Data/ if present
    try:
        summary, images = utils.generate_outputs(out_dir=out_dir)
        st.sidebar.success("Outputs regenerated")
    except Exception as e:
        st.sidebar.error(f"Failed to regenerate outputs: {e}")

if (out_dir / "summary_stats.csv").exists():
    try:
        summary = utils.read_summary(out_dir=out_dir)
        st.header("Summary statistics")
        st.dataframe(summary)
    except Exception as e:
        st.error(f"Failed to read summary: {e}")
else:
    st.info("No summary found in `outputs/`. Use the sidebar button to generate outputs from files in `Data/` or place `outputs/summary_stats.csv` here.")

st.header("Plots")
img_dir = out_dir
if img_dir.exists():
    pngs = sorted(img_dir.glob("*.png"))
    if pngs:
        cols = st.columns(2)
        for i, p in enumerate(pngs):
            with cols[i % 2]:
                st.image(str(p), caption=p.name)
    else:
        st.info("No plot images found in `outputs/`. Generate outputs to create plots.")
else:
    st.info("`outputs/` directory not found.")

st.markdown("---")
st.markdown("App created for quick cross-country comparisons. See `app/utils.py` for the data processing functions.")
