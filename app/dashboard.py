import sys
import os

# ---- Fix Python path for Streamlit ----
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(PROJECT_ROOT)

import streamlit as st
import pandas as pd
from ai.rules import assign_status

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Infrastructure Monitoring Dashboard",
    layout="wide",
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
/* App background */
.stApp {
    background-color: #f5f6f8;
    font-family: "Segoe UI", sans-serif;
}

/* KPI cards */
.kpi-card {
    background-color: white;
    padding: 20px;
    border-radius: 8px;
    text-align: center;
    box-shadow: 0 2px 6px rgba(0,0,0,0.05);
}

.kpi-title {
    font-size: 14px;
    color: #6c757d;
}

.kpi-value {
    font-size: 32px;
    font-weight: 600;
    margin-top: 5px;
    color: #212529;   /* dark readable color */
}


/* Section headers */
.section-title {
    font-size: 20px;
    font-weight: 600;
    margin-top: 30px;
    margin-bottom: 10px;
}

/* Table styling */
thead tr th {
    background-color: #f0f2f5 !important;
    color: #333 !important;
}

/* Footer note */
.footer {
    color: #888;
    font-size: 12px;
    margin-top: 20px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- LOAD DATA ----------------
DATA_PATH = "data/processed/projects.csv"
df = pd.read_csv(DATA_PATH)
df["status"] = df["progress_percent"].apply(assign_status)
# ---------------- ML: Delay Risk Prediction ----------------
from ml.predict import predict_delay_risk

# Encode sector for ML model
df["sector_encoded"] = df["sector"].apply(
    lambda x: 1 if x == "Railways" else 0
)

# Assumed elapsed ratio (since reports are monthly snapshots)
df["elapsed_ratio"] = 0.7

# Predict delay risk score
df["ml_delay_risk"] = df.apply(
    lambda r: predict_delay_risk(
        r["progress_percent"],
        r["sector_encoded"],
        r["elapsed_ratio"]
    ),
    axis=1
)

# Convert risk score to label
df["ML Risk Level"] = df["ml_delay_risk"].apply(
    lambda x: "High Risk" if x > 0.6 else "Low Risk"
)


# ---------------- HEADER ----------------
st.markdown("## Infrastructure Monitoring Dashboard")
st.markdown(
    "<span style='color:#6c757d'>AI-powered monitoring of government infrastructure projects</span>",
    unsafe_allow_html=True
)

# ---------------- KPI CARDS ----------------
total_projects = len(df)
delayed = (df["status"] == "Delayed").sum()
at_risk = (df["status"] == "At Risk").sum()
on_track = (df["status"] == "On Track").sum()

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">TOTAL PROJECTS</div>
        <div class="kpi-value">{total_projects}</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">DELAYED</div>
        <div class="kpi-value" style="color:#dc3545">{delayed}</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">AT RISK</div>
        <div class="kpi-value" style="color:#fd7e14">{at_risk}</div>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">ON TRACK</div>
        <div class="kpi-value" style="color:#28a745">{on_track}</div>
    </div>
    """, unsafe_allow_html=True)

# ---------------- PROJECT TABLE ----------------
st.markdown("<div class='section-title'>Project Progress Status</div>", unsafe_allow_html=True)

def comment_logic(status):
    if status == "Delayed":
        return "Critical delay"
    elif status == "At Risk":
        return "Needs monitoring"
    return "Progressing smoothly"

df["Comment"] = df["status"].apply(comment_logic)

table_df = df[[
    "project_name",
    "sector",
    "progress_percent",
    "status",
    "Comment"
]].rename(columns={
    "project_name": "Activity / Project",
    "sector": "Sector",
    "progress_percent": "% Complete",
    "status": "Status"
})

st.dataframe(table_df, use_container_width=True)

st.markdown("<div class='section-title'>ML-Based Delay Risk Prediction</div>", unsafe_allow_html=True)

st.dataframe(
    df[["project_name", "progress_percent", "ML Risk Level"]],
    use_container_width=True
)


# ---------------- CHARTS ----------------
st.markdown("<div class='section-title'>Project Analytics</div>", unsafe_allow_html=True)

g1, g2 = st.columns(2)

with g1:
    st.markdown("**Status Distribution**")
    st.bar_chart(df["status"].value_counts())

with g2:
    st.markdown("**Progress Distribution**")
    st.bar_chart(df["progress_percent"].value_counts().sort_index())

# ---------------- GEO ACTIVITY ----------------
st.markdown("<div class='section-title'>Geo Activity</div>", unsafe_allow_html=True)

st.info(
    "Illustrative geo activity based on regional project distribution. "
    "Exact coordinates will be enabled when available."
)

geo_df = pd.DataFrame({
    "lat": [28.61, 19.07, 12.97, 22.57],
    "lon": [77.20, 72.87, 77.59, 88.36]
})

st.map(geo_df)

# ---------------- FOOTER ----------------
st.markdown(
    "<div class='footer'>Data Source: Government Infrastructure Progress Reports (PAIMANA / Railways)</div>",
    unsafe_allow_html=True
)
