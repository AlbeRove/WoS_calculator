import streamlit as st
import pandas as pd

st.set_page_config(page_title="Upgrade Cost Calculator", page_icon="📈")

st.title("📈 Building Upgrade Calculator with Bonuses & Skills")

st.markdown("Calculate the total cost and time to upgrade a building with various skill and construction bonuses.")

# --- Base Upgrade Inputs ---

st.header("🏗️ Base Upgrade Parameters")

base_cost = st.number_input("Base Cost (Level 1)", value=100)
cost_multiplier = st.number_input("Cost Multiplier (per level)", value=1.15, step=0.01)
time_per_level = st.number_input("Time per Level (minutes)", value=5)
start_level = st.number_input("Start Level", min_value=1, value=1)
end_level = st.number_input("End Level", min_value=start_level, value=10)

st.markdown("---")

# --- Bonuses & Skills ---

st.header("🎖️ Bonuses & Skills")

zinman_level = st.selectbox(
    "Zinman Skill Level",
    options=[0, 1, 2, 3, 4, 5],
    index=0,
    format_func=lambda x: f"Level {x}"
)
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

base_construction_bonus = st.number_input(
    "Base Construction Speed Bonus (%)",
    min_value=0.0,
    value=0.0,
    step=0.1,
    format="%.1f"
)

president_skill = st.checkbox("President Skill Activated? (+10% speed bonus)", value=False)
vice_president_skill = st.checkbox("Vice President Skill Activated? (+10% speed bonus)", value=False)

speed_bonus_percent_president = 10 if president_skill else 0
speed_bonus_percent_vice_president = 10 if vice_president_skill else 0

double_time = st.checkbox("Double Construction Time (20% bonus)", value=False)

# Show bonuses summary
st.markdown(f"- Zinman Speed Bonus: **{speed_bonus_percent_zinman}%**")
st.markdown(f"- Zinman Cost Reduction: **{cost_bonus_percent_zinman}%**")
st.markdown(f"- Pet Speed Bonus: **{speed_bonus_percent_pet}%**" if pet_activated else "- Pet Speed Bonus: **N/A**")
st.markdown(f"- Base Construction Bonus: **{base_construction_bonus}%**")
st.markdown(f"- President Skill Bonus: **{speed_bonus_percent_president}%**")
st.markdown(f"- Vice President Skill Bonus: **{speed_bonus_percent_vice_president}%**")
st.markdown(f"- Double Construction Time: **{'Yes' if double_time else 'No'}**")

st.markdown("---")

# --- Calculation ---

levels = list(range(start_level, end_level + 1))

raw_costs = [base_cost * (cost_multiplier ** (lvl - 1)) for lvl in levels]
raw_times = [time_per_level for _ in levels]

adjusted_costs = [cost * (1 - cost_bonus_percent_zinman / 100) for cost in raw_costs]

total_speed_bonus_percent = (
    speed_bonus_percent_zinman +
    speed_bonus_percent_pet +
    base_construction_bonus +
    speed_bonus_percent_president +
    speed_bonus_percent_vice_president
)

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
st.caption("Adjust parameters and bonuses above.")
