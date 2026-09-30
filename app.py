import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

from src.models import SimulationAsset, AssetVariable
from src.engine import run_simulation
from src.analytics import calculate_stats

# Page config
st.set_page_config(page_title="Monte Carlo Simulator", layout="wide")

st.title("📈 Monte Carlo Financial Simulation Engine")
st.write("Simulate asset price paths driven by modular percentage variables using Geometric Brownian Motion.")

# --- Sidebar Inputs ---
st.sidebar.header("Asset Configuration")
asset_name = st.sidebar.text_input("Asset Name", value="House")
initial_value = st.sidebar.number_input("Initial Value (£)", value=300000.0, step=10000.0)

st.sidebar.header("Simulation Parameters")
years = st.sidebar.slider("Time Horizon (Years)", min_value=0.5, max_value=10.0, value=1.0, step=0.5)
n_paths = st.sidebar.slider("Number of Paths", min_value=100, max_value=5000, value=1000, step=100)
n_steps = st.sidebar.slider("Steps per Year (Trading Days)", min_value=50, max_value=365, value=252, step=1)

st.sidebar.header("Variables (Drivers)")
st.sidebar.subheader("Variable 1: Rental Income")
rent_return = st.sidebar.slider("Rent Expected Return", -0.20, 0.30, 0.10, 0.01)
rent_vol = st.sidebar.slider("Rent Volatility (S.D.)", 0.0, 0.20, 0.03, 0.005)

st.sidebar.subheader("Variable 2: Maintenance Cost")
maint_return = st.sidebar.slider("Maintenance Expected Return", -0.20, 0.20, -0.02, 0.01)
maint_vol = st.sidebar.slider("Maintenance Volatility (S.D.)", 0.0, 0.20, 0.01, 0.005)

# --- Run Simulation ---
# Build the asset container
asset = SimulationAsset(name=asset_name, initial_value=initial_value)
asset.add_varibes(AssetVariable("Rental Income", rent_return, rent_vol))
asset.add_varibes(AssetVariable("Maintenance", maint_return, maint_vol))

# Execute engine
paths = run_simulation(asset, years=years, n_steps=int(n_steps * years), n_paths=int(n_paths))
stats = calculate_stats(paths)

# --- Display Results ---
st.subheader("📊 Key Metrics (Terminal Outcomes)")
col1, col2, col3, col4 = st.columns(4)

col1.metric("Expected Value (Mean)", f"£{stats['mean_value']:,.0f}")
col2.metric("Median Value (50th %)", f"£{stats['median_value']:,.0f}")
col3.metric("5th Percentile (Risk)", f"£{stats['p5']:,.0f}")
col4.metric("95th Percentile (Gain)", f"£{stats['p95']:,.0f}")

# --- Plotting Paths ---
st.subheader("📉 Simulated Price Paths")
fig, ax = plt.subplots(figsize=(10, 5))

# Plot a subset of paths (e.g., first 100) to keep rendering fast and clean
ax.plot(paths[:, :100], color='skyblue', alpha=0.15)
# Plot median path or initial line
ax.axhline(initial_value, color='red', linestyle='--', label=f'Initial Value (£{initial_value:,.0f})')

ax.set_title(f"Monte Carlo Simulation for {asset_name} ({n_paths} Paths)")
ax.set_xlabel("Time Steps")
ax.set_ylabel("Asset Value (£)")
ax.legend()
ax.grid(True, alpha=0.3)

st.pyplot(fig)