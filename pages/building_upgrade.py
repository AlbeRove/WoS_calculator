import streamlit as st
import pandas as pd
from datetime import timedelta
import os

st.set_page_config(page_title="Upgrade Cost Calculator", page_icon="📈")

# --- Helper functions ---

def format_seconds(seconds: float) -> str:
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

# --- Zinman cost multipliers ---

zinman_cost_reduction = {
    0: 1.00,
    1: 0.97,
    2: 0.94,
    3: 0.91,
    4: 0.88,
    5: 0.85,
}

# --- Bonuses & Skills Section ---

st.title("📈 Building Upgrade Calculator with Bonuses & Skills")
st.markdown("Set your bonuses first, then select buildings and upgrade parameters.")

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

# zinman_active = st.checkbox("Activate Zinman Skill?", value=False)
# if zinman_active:
#     zinman_level = st.selectbox(
#         "Zinman Skill Level",
#         options=[0, 1, 2, 3, 4, 5],
#         index=0,
#         format_func=lambda x: f"Level {x}"
#     )
# else:
#     zinman_level = 0
zinman_level = st.radio(
    "Zinman Skill Level",
    options=[0, 1, 2, 3, 4, 5],
    index=0,
    format_func=lambda x: f"{x}" if x > 0 else "0 (None)",
    horizontal=True
)

st.write(f"Selected Zinman level: {zinman_level}")
# def zinman_level_selector():
#     st.write("Zinman Skill Level:")
#     cols = st.columns(5)
#     selected_level = 0
#     # Track which checkbox is selected
#     for i, col in enumerate(cols, start=1):
#         checked = st.session_state.get(f"zinman_level_chk_{i}", False)
#         new_val = col.checkbox(str(i), value=checked, key=f"zinman_level_chk_{i}")
#         if new_val:
#             selected_level = i
#             # Uncheck all others
#             for j in range(1, 6):
#                 if j != i:
#                     st.session_state[f"zinman_level_chk_{j}"] = False
#             break
#     return selected_level

# zinman_level = zinman_level_selector()
# st.write(f"Selected Zinman level: {zinman_level}")

speed_bonus_percent_zinman = zinman_level * 3
cost_bonus_percent_zinman = zinman_cost_reduction[zinman_level]

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
double_time = st.checkbox("Double Construction Time (20% bonus)", value=False)

speed_bonus_percent_president = 10 if president_skill else 0
speed_bonus_percent_vice_president = 10 if vice_president_skill else 0
speed_bonus_double_time = 20 if double_time else 0

# Calculate total speed bonus
total_speed_bonus_percent = (
    base_construction_bonus +
    speed_bonus_percent_zinman +
    speed_bonus_percent_pet +
    speed_bonus_percent_president +
    speed_bonus_percent_vice_president +
    speed_bonus_double_time
)

# Simple tooltip text
tooltip_text = "Click to see bonus breakdown below."

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

# --- Buildings selection ---

building_names = [
    "Furnace",
    "Embassy",
    "Infantry Camp",
    "Marksman Camp",
    "Lancer Camp",
    "Command Center",
    "Infirmary"
]

# Initialize session_state for active_buildings if not set
if "active_buildings" not in st.session_state:
    st.session_state.active_buildings = []

st.header("🏗️ Select Buildings to Upgrade")

cols = st.columns(3)
active_buildings = []
for idx, b in enumerate(building_names):
    toggled = cols[idx % 3].toggle(b, key=f"toggle_{b}")
    if toggled:
        active_buildings.append(b)

st.session_state.active_buildings = active_buildings

if not st.session_state.active_buildings:
    st.info("Please activate at least one building to upgrade.")
    st.stop()

# --- Upgrade levels selection ---

upgrade_selections = {}
for bname in st.session_state.active_buildings:
    st.subheader(bname)
    df = load_building_data(bname)
    if df is None:
        continue

    levels = df["level"].tolist()
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

if not upgrade_selections:
    st.info("Please select valid upgrade levels.")
    st.stop()

# --- Calculate button ---

if st.button("Calculate Upgrades"):

    resources = ["meat", "wood", "coal", "iron", "firecrystals"]
    total_resources = pd.Series(dtype=float)
    total_base_time = 0.0

    for bname, (cur_lvl, tgt_lvl, df) in upgrade_selections.items():
        upgrade_df = df[(df["level"] >= cur_lvl) & (df["level"] < tgt_lvl)]
        if upgrade_df.empty:
            continue

        # Apply Zinman cost reduction
        zinman_cost_multiplier = cost_bonus_percent_zinman
        cost_df = upgrade_df[resources] * zinman_cost_multiplier

        total_resources = total_resources.add(cost_df.sum(), fill_value=0)
        total_base_time += upgrade_df["time"].sum()

    # Apply speed bonus to time, including double time option
    reduction = 1 / (1 + total_speed_bonus_percent / 100)
    final_time = total_base_time * reduction
    if double_time:
        final_time *= 2

    # Format output nicely
    total_resources = total_resources.fillna(0).astype(int)
    total_time_str = format_seconds(final_time)

    # Display results in a nice table
    st.header("🧾 Total Upgrade Summary")

    result_df = pd.DataFrame({
        "Resource": [r.capitalize() for r in resources] + ["Time"],
        "Total Cost": [total_resources[r] for r in resources] + [total_time_str]
    })

    # Display costs as numbers, time as string
    # Show in the order: meat, wood, coal, iron, fire crystals, time
    st.table(result_df.set_index("Resource"))

