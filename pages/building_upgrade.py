import streamlit as st
import pandas as pd
from datetime import timedelta
import os

st.set_page_config(page_title="Upgrade Cost Calculator", page_icon="📈")

# --- Functions ---
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

# --- Bonus Section ---
st.title("📈 Building Upgrade Calculator with Bonuses & Skills")
st.markdown("Set your bonuses first, then select buildings to analyze.")

st.header("🎖️ Bonuses & Skills")

base_construction_bonus_str = st.text_input(
    "Base Construction Speed Bonus (%) - e.g. 5 or 12.5", value="0"
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
zinman_level = st.selectbox("Zinman Skill Level", options=list(range(6)), index=0, disabled=not zinman_active)
speed_bonus_percent_zinman = zinman_level * 3
cost_bonus_percent_zinman = zinman_level * 3

zinman_cost_multiplier_map = {
    0: 1.00,
    1: 0.97,
    2: 0.94,
    3: 0.91,
    4: 0.88,
    5: 0.85,
}
zinman_cost_multiplier = zinman_cost_multiplier_map.get(zinman_level, 1.0)

pet_activated = st.checkbox("Pet Activated?", value=False)
pet_level = st.selectbox("Pet Skill Level", options=list(range(1, 6)), index=0, disabled=not pet_activated)
pet_speed_bonuses = [0, 5, 7, 9, 12, 15]
speed_bonus_percent_pet = pet_speed_bonuses[pet_level] if pet_activated else 0

president_skill = st.checkbox("President Skill Activated? (+10% speed bonus)", value=False)
vice_president_skill = st.checkbox("Vice President Skill Activated? (+10% speed bonus)", value=False)

speed_bonus_percent_president = 10 if president_skill else 0
speed_bonus_percent_vice_president = 10 if vice_president_skill else 0

total_speed_bonus_percent = (
    base_construction_bonus +
    speed_bonus_percent_zinman +
    speed_bonus_percent_pet +
    speed_bonus_percent_president +
    speed_bonus_percent_vice_president
)

st.markdown("---")
st.markdown(
    f"### Total Speed Bonus: **{total_speed_bonus_percent:.2f}%**, Zinman Cost Multiplier: **{zinman_cost_multiplier:.2f}x**"
)

# --- Building Selection ---
st.header("🏗️ Building Selection")

building_names = [
    "Furnace",
    "Embassy",
    "Infantry Camp",
    "Marksman Camp",
    "Lancer Camp",
    "Command Center",
    "Infirmary"
]

selected_buildings = []
st.markdown("Click building names to include them in upgrade calculation.")

cols = st.columns(3)
for i, bname in enumerate(building_names):
    if cols[i % 3].button(bname, key=bname):
        if bname not in selected_buildings:
            selected_buildings.append(bname)

if not selected_buildings:
    st.info("No building selected.")
    st.stop()

# --- Upgrade Logic ---
upgrade_selections = {}
for bname in selected_buildings:
    st.subheader(bname)
    df = load_building_data(bname)
    if df is None:
        continue
    levels = df["level"].tolist()
    col1, col2 = st.columns(2)
    with col1:
        current_level = st.selectbox(f"{bname} Current Level", options=levels, index=0, key=f"{bname}_curr")
    with col2:
        possible_targets = [lvl for lvl in levels if lvl > current_level]
        if not possible_targets:
            st.warning(f"No higher target levels for {bname}")
            continue
        target_level = st.selectbox(f"{bname} Target Level", options=possible_targets, key=f"{bname}_target")
    upgrade_selections[bname] = (current_level, target_level, df)

# --- Totals ---
available_resources = ["meat", "wood", "coal", "iron", "firecrystals"]
total_resources = pd.Series(dtype=float)
total_base_time = 0.0

for bname, (cur_lvl, tgt_lvl, df) in upgrade_selections.items():
    upgrade_df = df[(df["level"] >= cur_lvl) & (df["level"] < tgt_lvl)]
    if upgrade_df.empty:
        continue
    res_sum = (upgrade_df[available_resources] * zinman_cost_multiplier).sum()
    total_resources = total_resources.add(res_sum, fill_value=0)
    total_base_time += upgrade_df["time"].sum()

# Apply speed bonus
reduction = 1 / (1 + total_speed_bonus_percent / 100)
final_time = total_base_time * reduction

# --- Output ---
st.header("🧾 Total Upgrade Summary")
st.subheader("🌿 Total Resource Costs")
for resource, amount in total_resources.items():
    st.markdown(f"- **{resource.capitalize()}**: {int(amount):,}")

st.subheader("⏳ Total Upgrade Time")
st.markdown(f"- **Base Time:** {format_seconds(total_base_time)}")
st.markdown(f"- **Adjusted Time:** {format_seconds(final_time)} _(after {total_speed_bonus_percent:.2f}% speed bonus)_")

st.markdown("---")
st.caption("Upload CSVs to the 'data' folder with columns: level, meat, wood, coal, iron, firecrystals, time")
