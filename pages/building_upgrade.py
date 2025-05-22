import streamlit as st
import pandas as pd
import os
from datetime import timedelta

st.set_page_config(page_title="Upgrade Cost Calculator", page_icon="📈")

st.title("📈 Building Upgrade Calculator with Bonuses & Skills")
st.markdown("Set your bonuses first, then select buildings to upgrade.")

# --- Bonuses & Skills ---

st.header("🎖️ Bonuses & Skills")

base_construction_bonus_str = st.text_input(
    "Base Construction Speed Bonus (%) - type a number, e.g. 5 or 12.5",
    value="0"
)

try:
    base_construction_bonus = float(base_construction_bonus_str)
    if base_construction_bonus < 0:
        st.warning("Base Construction Speed Bonus cannot be negative. Reset to 0.")
        base_construction_bonus = 0.0
except ValueError:
    st.warning("Invalid input for Base Construction Speed Bonus. Reset to 0.")
    base_construction_bonus = 0.0

zinman_active = st.checkbox("Activate Zinman Skill?", value=False)
if zinman_active:
    zinman_level = st.selectbox(
        "Zinman Skill Level",
        options=[0, 1, 2, 3, 4, 5],
        index=0,
        format_func=lambda x: f"Level {x}"
    )
else:
    zinman_level = 0

speed_bonus_percent_zinman = zinman_level * 3
cost_bonus_percent_zinman = zinman_level * 3

pet_activated = st.checkbox("Pet Activated?", value=False)
if pet_activated:
    pet_level = st.selectbox(
        "Pet Skill Level",
        options=[1, 2, 3, 4, 5],
        index=0,
        format_func=lambda x: f"Level {x}"
    )
else:
    pet_level = 0
pet_speed_bonuses = [0, 5, 7, 9, 12, 15]
speed_bonus_percent_pet = pet_speed_bonuses[pet_level]

president_skill = st.checkbox("President Skill Activated? (+10% speed bonus)", value=False)
vice_president_skill = st.checkbox("Vice President Skill Activated? (+10% speed bonus)", value=False)

speed_bonus_percent_president = 10 if president_skill else 0
speed_bonus_percent_vice_president = 10 if vice_president_skill else 0

double_time = st.checkbox("Double Construction Time (20% bonus)", value=False)

# Calculate total speed bonus (for time reduction)
total_speed_bonus_percent = (
    base_construction_bonus +
    speed_bonus_percent_zinman +
    speed_bonus_percent_pet +
    speed_bonus_percent_president +
    speed_bonus_percent_vice_president
)

# Tooltip breakdown text
tooltip_text = (
    f"Base Bonus: {base_construction_bonus:.2f}%\n"
    f"Zinman Speed Bonus: {speed_bonus_percent_zinman}%\n"
    f"Pet Speed Bonus: {speed_bonus_percent_pet if pet_activated else 'N/A'}%\n"
    f"President Skill: {speed_bonus_percent_president}%\n"
    f"Vice President Skill: {speed_bonus_percent_vice_president}%\n"
    f"Total: {total_speed_bonus_percent:.2f}%"
)

# Display Total Speed Bonus with tooltip
st.markdown("---")
st.markdown(
    f"### Total Speed Bonus: "
    f"<span title='{tooltip_text}' style='text-decoration: underline; cursor: help;'>"
    f"{total_speed_bonus_percent:.2f}%"
    f"</span>",
    unsafe_allow_html=True
)

with st.expander("🔍 See bonus breakdown"):
    st.markdown(f"- Base Bonus: **{base_construction_bonus:.2f}%**")
    st.markdown(f"- Zinman Speed Bonus: **{speed_bonus_percent_zinman}%**")
    st.markdown(f"- Pet Speed Bonus: **{speed_bonus_percent_pet if pet_activated else 0}%**")
    st.markdown(f"- President Skill: **{speed_bonus_percent_president}%**")
    st.markdown(f"- Vice President Skill: **{speed_bonus_percent_vice_president}%**")
st.markdown("---")

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

# Use checkboxes as toggle buttons for each building
activated_buildings = []
for bname in building_names:
    if st.checkbox(f"Activate {bname}", key=f"activate_{bname}"):
        activated_buildings.append(bname)

if not activated_buildings:
    st.info("Please activate at least one building to upgrade.")
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

# Apply speed bonus to total time
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
