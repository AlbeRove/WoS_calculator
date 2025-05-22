import streamlit as st
import pandas as pd

st.set_page_config(page_title="Upgrade Cost Calculator", page_icon="📈")

st.title("📈 Building Upgrade Calculator with Bonuses & Skills")

st.markdown("Set your bonuses first, then define building upgrade parameters.")

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

total_speed_bonus_percent = (
    base_construction_bonus +
    speed_bonus_percent_zinman +
    speed_bonus_percent_pet +
    speed_bonus_percent_president +
    speed_bonus_percent_vice_president
)

# Compose tooltip text with breakdown
tooltip_text = (
    f"Breakdown of Speed Bonuses:\n"
    f"- Base Construction Bonus: {base_construction_bonus:.2f}%\n"
    f"- Zinman Speed Bonus: {speed_bonus_percent_zinman}%\n"
    f"- Pet Speed Bonus: {speed_bonus_percent_pet if pet_activated else 'N/A'}%\n"
    f"- President Skill Bonus: {speed_bonus_percent_president}%\n"
    f"- Vice President Skill Bonus: {speed_bonus_percent_vice_president}%\n"
    f"- Total: {total_speed_bonus_percent:.2f}%"
)

st.markdown("---")
# Show only total speed bonus with hover tooltip
st.markdown(
    f"### Total Speed Bonus: "
    f"<span title='{tooltip_text}' style='text-decoration: underline; cursor: help;'>"
    f"**{total_speed_bonus_percent:.2f}%**"
    f"</span>",
    unsafe_allow_html=True
)
st.markdown("---")

# --- Base Upgrade Inputs ---

st.header("🏗️ Base Upgrade Parameters")

base_cost = st.number_input("Base Cost (Level 1)", value=100)
cost_multiplier = st.number_input("Cost Multiplier (per level)", value=1.15, step=0.01)
time_per_level = st.number_input("Time per Level (minutes)", value=5)
start_level = st.number_input("Start Level", min_value=1, value=1)
end_level = st.number_input("End Level", min_value=start_level, value=10)

# --- Calculation ---

levels = list(range(start_level, end_level + 1))

raw_costs = [base_cost * (cost_multiplier ** (lvl - 1)) for lvl in levels]
raw_times = [time_per_level for _ in levels]

adjusted_costs = [cost * (1 - cost_bonus_percent_zinman / 100) for cost in raw_costs]

if double_time:
    adjusted_times = [time * 2 for time in raw_times]
else:
    adjusted_times = raw_times.copy()

adjusted_times = [time * (1 - total_speed_bonus_percent / 100) for time in adjusted_times]

total_cost = int(sum(adjusted_costs))
total_time = int(sum(adjusted_times))

df = pd.DataFrame({
    "Level": levels,
    "Base Cost": [int(c) for c in raw_costs],
    "Adjusted Cost": [int(c) for c in adjusted_costs],
    "Base Time (min)": raw_times,
    "Adjusted Time (min)": [round(t, 2) for t in adjusted_times]
})

# --- Output ---

st.subheader("📊 Upgrade Summary")

st.write(f"**Total cost** from level {start_level} to {end_level}: **{total_cost}** coins (after Zinman bonus)")
st.write(f"**Total time**: **{total_time}** minutes (after bonuses and time modifiers)")

st.dataframe(df, use_container_width=True)

st.markdown("---")
st.caption("Adjust bonuses and upgrade parameters above.")
