import streamlit as st
import pandas as pd


if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("Please log in to access this page")
    st.stop()

st.title("📊 Dashboard")

st.title("Welcome Lads!")  # Dashboard title

try:
    df_incidents = pd.read_csv("DATA/cyber_incidents.csv")
except FileNotFoundError:
    st.error("Could not find DATA/cyber_incidents.csv")
    st.stop()

df_incidents.columns = df_incidents.columns.str.strip()

st.subheader("Cyber Incidents Summary")
col1, col2, col3 = st.columns(3)
col1.metric("High Severity", df_incidents[df_incidents["severity"] == "High"].shape[0])
col2.metric("Medium Severity", df_incidents[df_incidents["severity"] == "Medium"].shape[0])
col3.metric("Total Incidents", df_incidents.shape[0])

st.subheader("Cyber Incidents Table")
st.dataframe(df_incidents)

severity_counts = df_incidents["severity"].value_counts().reset_index()
severity_counts.columns = ["Severity Type", "Count"]

st.subheader("Incidents by Severity")
st.bar_chart(data=severity_counts.set_index("Severity Type"))
