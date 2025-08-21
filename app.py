import streamlit as st
import pandas as pd
from simulator import load_data, simulate_risks, calculate_kpis

# Load data
df = load_data()

# Title
st.title("📦 Supply Chain Risk Simulator")
st.markdown("Model demand surges, supplier delays, and transport costs to evaluate supply chain risks.")

# Sliders
demand = st.slider("Demand Surge (%)", 0, 100, 20) / 100
delay = st.slider("Supplier Delay (days)", 0, 10, 2)
transport = st.slider("Transport Cost Increase (%)", 0, 50, 10) / 100

# Run simulation
simulated = simulate_risks(df, demand, delay, transport)

# KPIs
st.subheader("📊 KPI Comparison")
base_kpis = calculate_kpis(df)
sim_kpis = calculate_kpis(simulated)
col1, col2 = st.columns(2)
with col1:
    st.write("**Base**", base_kpis)
with col2:
    st.write("**Simulated**", sim_kpis)

# Supplier Performance
st.subheader("🚚 Supplier On-Time Performance")
supplier_perf = simulated.groupby("Supplier")["OnTime"].value_counts(normalize=True).unstack().fillna(0) * 100
st.bar_chart(supplier_perf["Yes"])

# Regional Costs
st.subheader("🌍 Cost Distribution by Region")
region_costs = simulated.groupby("Region")["TotalCost"].sum()
st.bar_chart(region_costs)
