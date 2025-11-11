import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from app.utils import load_countries, summary_table

st.title('Cross-country Solar Comparison')

# Widget: select countries to include
available = list(load_countries().keys())
selected = st.multiselect('Select countries', available, default=available)

if not selected:
    st.warning('Select at least one country')
    st.stop()

# Load merged data for selected countries
dfs = {}
for c in selected:
    dfs[c] = load_countries()[c]

merged = pd.concat(dfs.values(), ignore_index=True, sort=False)

st.header('Summary table')
st.dataframe(summary_table(merged))

st.header('GHI boxplot')
fig, ax = plt.subplots(figsize=(8,4))
sns.boxplot(x='country', y='GHI', data=merged, ax=ax, palette='Set2')
ax.set_title('GHI by country')
st.pyplot(fig)

st.header('Top regions (by average GHI)')
if 'Region' in merged.columns:
    top_regions = merged.groupby(['country','Region'])['GHI'].mean().reset_index()
    top = top_regions.sort_values('GHI', ascending=False).head(10)
    st.table(top)
else:
    st.info('No `Region` column found in data — replace with your region field or add it in Data CSVs')

st.markdown('---')
st.markdown('Notes: Data files are expected in `Data/<country>_clean.csv`. The app reads them locally.')