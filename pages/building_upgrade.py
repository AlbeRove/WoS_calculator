import streamlit as st
import pandas as pd

st.set_page_config(page_title="Upgrade Cost Calculator", page_icon="📈")

st.title("📈 Building Upgrade Calculator with Zinman & Pet Skills")

st.markdown("Calculate the total cost and time to upgrade a building with Zinman and Pet skill bonuses.")

# --- Input Parameters ---

st.header("🔧 Upgrade Parameters")

base_cost = st.number_input("Base Cost (Level 1)", value=100)
cost_multiplier = st.number_input("Cost Multiplier (per level)", value=1.15, step=0.01)
time_per_level = st.number_input("Time per Level (minutes)", value=5)
start_level = st.number_input("Start Level", min_value=1, value=1)
end_level = st.number_input("End Level", min_value=start_level, value=10)

st.markdown("---")

st.header("🎖️ Zinman Skill Level")
zinman_level = st.select_slider(
    "Select Zinman skill level",
    options=[0, 1, 2, 3, 4, 5],
    value=0,
    format_func=lambda x: f"Level {x}"
)

# ...

st.header("🐾 Pet Skill")
pet_activated = st.checkbox("Pet Activated?", value=False)

if pet_activated:
    pet_level = st.select_slider(
        "Select Pet skill level",
        options=[1, 2, 3, 4, 5],
        value=1,
        format_func=lambda x: f"Level {x}"
    )
else:
    pet_level = 0

speed_bonus_percent_pet = pet_speed_bonuses[pet_level]

if pet_activated:
    st.markdown(f"**Pet Construction Speed Bonus:** {speed_bonus_percent_pet}%")
else:
    st.markdown("Pet Construction Speed Bonus: N/A")

st.markdown("---")

st.heade
