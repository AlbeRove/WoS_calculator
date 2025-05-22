import streamlit as st
import pandas as pd
import os
from datetime import timedelta

st.set_page_config(page_title="Upgrade Cost Calculator", page_icon="📈")

st.title("📈 Building Upgrade Calculator with Bonuses & Skills")
st.markdown("Set your bonuses first, then select buildings to upgrade.")

# --- Bonuses & Skills ---

# (Same bonus code as before)
# For brevity, I’ll skip repeating the bonus code here — assume you include it above exactly as before.

# --- Utility functions for multi-building part ---

def format_seconds(seconds: int) -> str:
    td = timedelta(seconds=int(seconds))
    days = td.days
    hours, remainder = divmod(td.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    if days > 0:
        return f"{days}d {hours:02d}:{minutes:02d}:{seconds:02d}"
    else:
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

def get_csv_filename(building_name: str) -> str:
    filename = building_name.lower().replace(" ", "") + ".csv"
    return os.path.join("data", filename)

def load_building_data(name):
    filename = get_csv_filename(name)
    try:
        return pd.read_csv(filename)
    except FileNotFoundError:
        st.warning(f"Data file '{filename}' for {name} not found in the 'data' folder.")
        return None

# --- Multi-building upgrade section ---

st.header("🏗️ Multi-Building Upgrade Calculator")

building_names = [
    "Furnace",
    "Embassy",
    "Infantry Camp",
    "Marksman Camp",
    "Lancer Camp",
    "Command Center",
    "Infirmary"
]

# Initialize session state for building toggles if not present
if "active_buildings" not in st.session_state:
    st.session_state.active_buildings = {bname: False for bname in building_names}

# Render buttons for each building
cols = st.columns(len(building_names))  # Put buttons side by side

for i, bname in enumerate(building_names):
    # Change button label based on active state with emoji
    label = f"✅ {bname}" if st.session_state.active_buildings[bname] else bname

    if cols[i].button(label):
        # Toggle state on click
        st.session_state.active_buildings[bname] = not st.session_state.active_buildings[bname]

# Collect active buildings
activated_buildings = [b for b, active in st.session_state.active_buildings.items() if active]

if not activated_buildings:
    st.info("Please activate at least one building by clicking its button.")
    st.stop()

upgrade_selections = {}

for bname in activated_buildings:
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

# Assuming total_speed_bonus_percent is calculated in your bonuses code above

total_resources = pd.Series(dtype=float)
total_base_time = 0.0

for bname, (cur_lvl, tgt_lvl, df) in upgrade_selections.items():
    upgrade_df = df[(df["level"] >= cur_lvl) & (df["level"] < tgt_lvl)]
    if upgrade_df.empty:
        continue
    resources = ["meat", "wood", "coal", "iron", "fire crystals"]
    res_sum = upgrade_df[resources].sum()
    total_resources = total_resources.add(res_sum, fill_value=0)
    total_base_time += upgrade_df["time"].sum()

reduction = 1 / (1 + total_speed_bonus_percent / 100)  # convert % to factor
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
