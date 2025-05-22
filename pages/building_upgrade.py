import streamlit as st
import pandas as pd
from datetime import timedelta
import os

st.set_page_config(page_title="Upgrade Cost Calculator", page_icon="📈")

# -------- Helper Functions --------
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
    return os.path.join("data", building_name.lower().replace(" ", "") + ".csv")

def load_building_data(name):
    filename = get_csv_filename(name)
    try:
        return pd.read_csv(filename)
    except FileNotFoundError:
        st.warning(f"Data file '{filename}' for {name} not found.")
        return None

# -------- UI: Bonuses --------
st.title("📈 Building Upgrade Calculator with Bonuses & Skills")
st.markdown("Set your bonuses first, then define building upgrade parameters.")

st.header("🎖️ Bonuses & Skills")

base_construction_bonus_str = st.text_input("Base Construction Speed Bonus (%)", value="0")

try:
    base_construction_bonus = float(base_construction_bonus_str)
    if base_construction_bonus < 0:
        st.warning("Base bonus cannot be negative. Reset to 0.")
        base_construction_bonus = 0.0
except ValueError:
    st.warning("Invalid input. Reset to 0.")
    base_construction_bonus = 0.0

zinman_active = st.checkbox("Activate Zinman Skill?")
zinman_level = 0
if zinman_active:
    zinman_level = st.selectbox("Zinman Skill Level", options=[0, 1, 2, 3, 4, 5], index=0)

zinman_speed_bonus = zinman_level * 3
zinman_cost_multiplier = [1.0, 0.97, 0.94, 0.91, 0.88, 0.85][zinman_level]

pet_activated = st.checkbox("Activate Pet Bonus?")
pet_level = 0
if pet_activated:
    pet_level = st.selectbox("Pet Skill Level", options=[1, 2, 3, 4, 5], index=0)

pet_speed_bonuses = [0, 5, 7, 9, 12, 15]
pet_speed_bonus = pet_speed_bonuses[pet_level]

president_skill = st.checkbox("President Skill Activated? (+10%)")
vice_president_skill = st.checkbox("Vice President Skill Activated? (+10%)")

speed_bonus_total = (
    base_construction_bonus +
    zinman_speed_bonus +
    pet_speed_bonus +
    (10 if president_skill else 0) +
    (10 if vice_president_skill else 0)
)

speed_multiplier = 1 / (1 + (speed_bonus_total / 100))

# -------- UI: Building Selection --------
st.header("🏗️ Select Buildings to Upgrade")

building_names = [
    "Furnace",
    "Embassy",
    "Infantry Camp",
    "Marksman Camp",
    "Lancer Camp",
    "Command Center",
    "Infirmary"
]

activated_buildings = []
cols = st.columns(3)
for idx, b in enumerate(building_names):
    if cols[idx % 3].button(b):
        activated_buildings.append(b)

if not activated_buildings:
    st.info("Please select at least one building.")
    st.stop()

# -------- Upgrade Inputs --------
upgrade_selections = {}
for bname in activated_buildings:
    st.subheader(f"⚙️ {bname}")
    df = load_building_data(bname)
    if df is None:
        continue

    levels = df["level"].tolist()
    min_level, max_level = min(levels), max(levels)

    col1, col2 = st.columns(2)
    with col1:
        current_level = st.selectbox(f"{bname} - Current Level", options=levels, index=0, key=f"{bname}_curr")
    with col2:
        target_options = [lvl for lvl in levels if lvl > current_level]
        if not target_options:
            st.warning("No levels above current.")
            continue
        target_level = st.selectbox(f"{bname} - Target Level", options=target_options, key=f"{bname}_target")

    upgrade_selections[bname] = (current_level, target_level, df)

# -------- Calculate Button --------
if st.button("🚀 Calculate Upgrades"):
    expected_resources = ["meat", "wood", "coal", "iron", "fire crystals"]
    total_resources = pd.Series(0.0, index=expected_resources)
    total_base_time = 0.0

    for bname, (cur_lvl, tgt_lvl, df) in upgrade_selections.items():
        upgrade_df = df[(df["level"] >= cur_lvl) & (df["level"] < tgt_lvl)]
        if upgrade_df.empty:
            continue

        # Ensure all expected columns exist
        for col in expected_resources:
            if col not in upgrade_df.columns:
                upgrade_df[col] = 0

        cost_df = upgrade_df[expected_resources] * zinman_cost_multiplier
        total_resources += cost_df.sum()
        total_base_time += upgrade_df["time"].sum()

    adjusted_time = total_base_time * speed_multiplier

    st.header("✅ Total Upgrade Summary")
    st.markdown(f"""
    **Meat**: `{int(total_resources['meat']):,}`  
    **Wood**: `{int(total_resources['wood']):,}`  
    **Coal**: `{int(total_resources['coal']):,}`  
    **Iron**: `{int(total_resources['iron']):,}`  
    **Fire Crystals**: `{int(total_resources['fire crystals']):,}`  
    **Time**: `{format_seconds(adjusted_time)}`
    """)
