import streamlit as st
import pandas as pd
from utils.mapping import create_map

st.set_page_config(layout="wide")

@st.cache_data(ttl=900)
def load_data():
    return pd.read_parquet("data/live_state.parquet")

df = load_data()

scada_time = pd.to_datetime(df["scada_timestamp"].iloc[0], utc=True)
now = pd.Timestamp.utcnow()
age = (now - scada_time).total_seconds() / 60

if age <= 20:
    status = "🟢 LIVE"
elif age <= 45:
    status = "🟠 DELAYED"
else:
    status = "🔴 STALE"

status_html = f"""
<div style="
    position: fixed;
    top: 30px;
    right: 30px;
    background: white;
    padding: 10px;
    border-radius: 8px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.3);
    z-index: 9999;
    font-size: 14px;
">
<b>SCADA Status:</b> {status}<br>
<small>
{scada_time.strftime('%Y-%m-%d %H:%M UTC')}<br>
Age: {age:.1f} min
</small>
</div>
"""

m = create_map(df, status_html)
st.components.v1.html(m._repr_html_(), height=750)
