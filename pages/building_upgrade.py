import streamlit as st
import pandas as pd
import os
from datetime import timedelta

# Format seconds to "Xd HH:MM:SS" or "HH:MM:SS"
def format_seconds(seconds: int) -> str:
    td = timedelta(seconds=int(seconds))
    days = td.days
    hours, remainder = divmod(td.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    if days > 0:
        return f"{days}d {hours:02d}:{minutes:02d}:{seconds:02d}"
    else:
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

# Get CSV filename inside data folder
def get_csv_filename(building_name: str) -> str:
    filename = building_name.lower().replace(" ", "") + ".csv"
    return os.path.join("data", filename)

# Load building upgrade data CSV
def load_building_data(name):
    filename = get_csv_filename(name)
    try:
        return pd.read_csv(filename)
    except FileNotFoundError:
        st.warning(f"Data file '{filename}' for {name} not found in the 'data' folder.")
        return None

st.title("🏗️ Multi-Building Upgrade Calculator")

# Building list
building_names = [
    "Furnace",
    "Embassy",
    "Infantry Camp",
    "Marksman Camp",
    "Lancer Camp",
    "Command Center",
    "Infirmary"
]

# Bonus input section
st.sidebar.header("⚡ Speed Bonus")
total_speed_bonus_percent = st.sidebar.number_input(
    "Enter total speed bonus (%)",
    min_value=0.0,
    max_value=100.0,
    value=0.0,
    step=0.1,
    help="Enter your total upgrade speed bonus percentage (e.g., from research or buffs)."
)

total_bonus = total_speed_bonus_percent / 100  # convert % to decimal

# Select buildings to upgrade
selected_buildings = st.multiselect("Select Buildings to Upgrade", building_names)

if not selected_buildings:
    st.info("Please select at least one building to upgrade.")
    st.stop()

# Dictionary to hold selections: {building_name: (current_level, target_level, df)}
upgrade_selections = {}

for bname in selected_buildings:
    st.subheader(bname)
    df = load_building_data(bname)
    if df is None:
        continue
    if "level" not in df.columns:
        st.error(f"Data file for {bname} missing 'level' column.")
        continue
    levels = sorted(df["level"].tolist())
    min_level, max_level = min(levels), max(levels)

    col1, col2 = st.columns(2)
    with col1:
        current_level = st.selectbox(f"{bname} Current Level", options=levels, index=0, key=f"{bname}_curr")
    with col2:
        possible_targets = [lvl for lvl in levels if lvl > current_level]
        if not possible_targets:
            st.warning(f"No higher target levels available for {bname}")
            continue
        target_level = st.selectbox(f"{bname} Target Level", options=possible_targets, key=f"{bname}_target")

    upgrade_selections[bname] = (current_level, target_level, df)

# Calculate total resources and total time
total_resources = pd.Series(dtype=float)
total_base_time = 0.0

for bname, (cur_lvl, tgt_lvl, df) in upgrade_selections.items():
    upgrade_df = df[(df["level"] >= cur_lvl) & (df["level"] < tgt_lvl)]
    if upgrade_df.empty:
        continue
    # Sum resources
    resources = ["meat", "wood", "coal", "iron", "fire crystals"]
    res_sum = upgrade_df[resources].sum()
    total_resources = total_resources.add(res_sum, fill_value=0)
    # Sum time
    total_base_time += upgrade_df["time"].sum()

# Apply speed bonus to time (reduce time)
reduction = 1 / (1 + total_bonus)
final_time = total_base_time * reduction

st.header("🧾 Total Upgrade Summary")

st.subheader("Total Resource Costs")
if total_resources.empty:
    st.write("No resources needed.")
else:
    for resource, amount in total_resources.items():
        st.write(f"- {resource.capitalize()}: {int(amount):,}")

st.subheader("Total Upgrade Time")
st.write(f"- Base time: {format_seconds(total_base_time)}")
st.write(f"- Adjusted time: {format_seconds(final_time)} (with {total_speed_bonus_percent:.2f}% speed bonus)")
