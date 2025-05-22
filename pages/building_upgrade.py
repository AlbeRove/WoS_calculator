import streamlit as st
import pandas as pd

st.set_page_config(page_title="Upgrade Cost Calculator", page_icon="📈")

st.title("📈 Building Upgrade Calculator with Zinman & Pet Skills")

st.markdown("Calculate the total cost and time to upgrade a building with Zinman and Pet skill bonuses.")

# --- Input Parameters ---
st.sidebar.header("🔧 Upgrade Parameters")

base_cost = st.sidebar.number_input("Base Cost (Level 1)", value=100)
cost_multiplier = st.sidebar.number_input("Cost Multiplier (per level)", value=1.15, step=0.01)
time_per_level = st.sidebar.number_input("Time per Level (minutes)", value=5)
start_level = st.sidebar.number_input("Start Level", min_value=1, value=1)
end_level = st.sidebar.number_input("End Level", min_value=start_level, value=10)

# Zinman skill level selector
st.sidebar.header("🎖️ Zinman Skill Level")
zinman_level = st.sidebar.slider("Select Zinman skill level", min_value=0, max_value=5, value=0)

speed_bonus_percent_zinman = zinman_level * 3  # 3% speed up per level
cost_bonus_percent_zinman = zinman_level * 3   # 3% cost down per level

st.sidebar.markdown(f"**Zinman Construction Speed Bonus:** {speed_bonus_percent_zinman}%")
st.sidebar.markdown(f"**Zinman Construction Cost Reduction:** {cost_bonus_percent_zinman}%")

# Pet skill activation and level
st.sidebar.header("🐾 Pet Skill")
pet_activated = st.sidebar.checkbox("Pet Activated?", value=False)

pet_speed_bonuses = [0, 5, 7, 9, 12, 15]  # index = pet level, 0 when not activated
pet_level = 1
if pet_activated:
    pet_level = st.sidebar.slider("Select Pet skill level", min_value=1, max_value=5, value=1)
else:
    pet_level = 0  # no bonus if not activated

speed_bonus_percent_pet = pet_speed_bonuses[pet_level]

if pet_activated:
    st.sidebar.markdown(f"**Pet Construction Speed Bonus:** {speed_bonus_percent_pet}%")
else:
    st.sidebar.markdown("Pet Construction Speed Bonus: N/A")

# Double time toggle
st.sidebar.header("⏳ Time Modifiers")
double_time = st.sidebar.checkbox("Double Construction Time (20% bonus)", value=False)

# --- Compute Upgrade Cost and Time ---
levels = list(range(start_level, end_level + 1))

# Calculate raw costs and times
raw_costs = [base_cost * (cost_multiplier ** (lvl - 1)) for lvl in levels]
raw_times = [time_per_level for _ in levels]

# Apply Zinman cost reduction
adjusted_costs = [cost * (1 - cost_bonus_percent_zinman / 100) for cost in raw_costs]

# Calculate combined speed bonus from Zinman and Pet (additive)
total_speed_bonus_percent = speed_bonus_percent_zinman + speed_bonus_percent_pet

# Apply double time modifier before speed reduction
if double_time:
    adjusted_times = [time * 2 for time in raw_times]
else:
    adjusted_times = raw_times.copy()

# Apply total speed bonus to reduce time
adjusted_times = [time * (1 - total_speed_bonus_percent / 100) for time in adjusted_times]

# Sum totals
total_cost = int(sum(adjusted_costs))
total_time = int(sum(adjusted_times))

# Prepare DataFrame for display
df = pd.DataFrame({
    "Level": levels,
    "Base Cost": [int(c) for c in raw_costs],
    "Adjusted Cost": [int(c) for c in adjusted_costs],
    "Base Time (min)": raw_times,
    "Adjusted Time (min)": [round(t,2) for t in adjusted_times]
})

# --- Output ---
st.subheader("📊 Upgrade Summary")

st.write(f"**Total cost** from level {start_level} to {end_level}: **{total_cost}** coins (after Zinman bonus)")
st.write(f"**Total time**: **{total_time}** minutes (after bonuses and time modifiers)")

st.dataframe(df, use_container_width=True)

st.markdown("---")
st.caption("Use the sidebar to adjust parameters, Zinman & Pet skill levels, and time modifiers.")
