import streamlit as st
import pandas as pd
import json
from pathlib import Path
from utils.mapping import create_map

# ------------------------------------------------------------------------------
# STREAMLIT CONFIG
# ------------------------------------------------------------------------------
st.set_page_config(
    layout="wide",
    page_title="AU Wind – Live SCADA Map"
)

# ------------------------------------------------------------------------------
# CACHED LOADERS
# ------------------------------------------------------------------------------

@st.cache_data(ttl=900)
def load_live_state():
    """
    Load the latest live SCADA-derived state used for the map.
    Expected to be refreshed every ~15 minutes by an external job.
    """
    return pd.read_parquet("data/live_state.parquet")


@st.cache_data
def load_training_window():
    """
    Load persisted model training window metadata.
    """
    path = Path("data/training_window.json")
    if not path.exists():
        return None
    return json.loads(path.read_text())


# ------------------------------------------------------------------------------
# LOAD DATA
# ------------------------------------------------------------------------------

df = load_live_state()
training_window = load_training_window()

# ------------------------------------------------------------------------------
# SCADA STATUS INDICATOR
# ------------------------------------------------------------------------------

scada_time = pd.to_datetime(df["scada_timestamp"].iloc[0], utc=True)
now = pd.Timestamp.utcnow()
age_min = (now - scada_time).total_seconds() / 60

if age_min <= 20:
    status = "🟢 LIVE"
elif age_min <= 45:
    status = "🟠 DELAYED"
else:
    status = "🔴 STALE"

status_html = f"""
<div style="
    position: fixed;
    top: 30px;
    right: 30px;
    background: white;
    padding: 10px 14px;
    border-radius: 8px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.3);
    z-index: 9999;
    font-size: 14px;
">
<b>SCADA Status:</b> {status}<br>
<small>
{scada_time.strftime('%Y-%m-%d %H:%M UTC')}<br>
Age: {age_min:.1f} min
</small>
</div>
"""

# ------------------------------------------------------------------------------
# SIDEBAR METADATA
# ------------------------------------------------------------------------------

with st.sidebar:
    st.header("Model Information")

    if training_window:
        st.markdown("**Training Window**")
        st.write(
            f"{training_window['first_date']} → {training_window['last_date']}"
        )
        st.caption(
            f"Trained at: {training_window['trained_at']}"
        )
    else:
        st.warning("Training metadata not available")

    st.markdown("---")
    st.caption("AU Windfarms – Live SCADA & Power Curves")

# ------------------------------------------------------------------------------
# MAP RENDERING
# ------------------------------------------------------------------------------

m = create_map(df, status_html)

st.components.v1.html(
    m._repr_html_(),
    height=750,
    scrolling=False
)