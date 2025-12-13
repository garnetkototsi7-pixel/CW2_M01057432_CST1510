import streamlit as st
import pandas as pd

st.title("Welcome Lads!")  # Dashboard title

# --- Load cyber incidents data ---
try:
    df_incidents = pd.read_csv("DATA/cyber_incidents.csv")
except FileNotFoundError:
    st.error("Could not find DATA/cyber_incidents.csv")
    st.stop()

# Clean column names
df_incidents.columns = df_incidents.columns.str.strip()

# --- Metrics ---
st.subheader("Cyber Incidents Summary")
col1, col2, col3 = st.columns(3)
col1.metric("High Severity", df_incidents[df_incidents["severity"] == "High"].shape[0])
col2.metric("Medium Severity", df_incidents[df_incidents["severity"] == "Medium"].shape[0])
col3.metric("Total Incidents", df_incidents.shape[0])

# --- Cyber Incidents Table ---
st.subheader("Cyber Incidents Table")
st.dataframe(df_incidents)

# --- Incidents by Severity Bar Chart ---
severity_counts = df_incidents["severity"].value_counts().reset_index()
severity_counts.columns = ["Severity Type", "Count"]

st.subheader("Incidents by Severity")
st.bar_chart(data=severity_counts.set_index("Severity Type"))
