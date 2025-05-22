import streamlit as st
import pandas as pd

st.set_page_config(page_title="Upgrade Cost Calculator", page_icon="📈")

st.title("📈 Building Upgrade Calculator")
st.markdown("Calculate the total cost and time to upgrade a building through multiple levels.")

# --- Input Parameters ---
st.sidebar.header("🔧 Upgrade Parameters")

base_cost = st.sidebar.number_input("Base Cost (Level 1)", value=100)
cost_multiplier = st.sidebar.number_input("Cost Multiplier (per level)", value=1.15, step=0.01)
time_per_level = st.sidebar.number_input("Time per Level (minutes)", value=5)
start_level = st.sidebar.number_input("Start Level", min_value=1, value=1)
end_level = st.sidebar.number_input("End Level", min_value=start_level, value=10)

# --- Compute Upgrade Cost and Time ---
levels = list(range(start_level, end_level + 1))
costs = [int(base_cost * (cost_multiplier ** (lvl - 1))) for lvl in levels]
times = [lvl * time_per_level for lvl in range(1, len(levels) + 1)]

df = pd.DataFrame({
    "Level": levels,
    "Upgrade Cost": costs,
    "Upgrade Time (min)": times
})

total_cost = sum(costs)
total_time = sum(times)

# --- Output ---
st.subheader("📊 Upgrade Summary")

st.write(f"**Total cost** from level {start_level} to {end_level}: `{total_cost}` coins")
st.write(f"**Total time**: `{total_time}` minutes")

st.dataframe(df, use_container_width=True)

st.markdown("---")
st.caption("Pro tip: use the sidebar to tweak values for different buildings.")

