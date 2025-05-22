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
zinman_level = st.slider("Select Zinman skill level", min_value=0, max_value=5, value=0)

speed_bonus_percent_zinman = zinman_level * 3  # 3% speed up per level
cost_bonus_percent_zinman = zinman_level * 3   # 3% cost down per level

st.markdown(f"**Zinman Construction Speed Bonus:** {speed_bonus_percent_zinman}%")
st.markdown(f"**Zinman Construction Cost Reduction:** {cost_bonus_percent_zinman}%")

st.markdown("---")

st.header("🐾 Pet Skill")
pet_activated = st.checkbox("Pet Activated?", value=False)

pet_speed_bonuses = [0, 5, 7, 9, 12, 15]  # index = pet level, 0 if not activated
pet_level = 1
if pet_activated:
    pet_level = st.slider("Select Pet skill level", min_value=1, max_value=5, value=1)
else:
    pet_level = 0  # no bonus if not activated

speed_bonus_percent_pet = pet_speed_bonuses[pet_level]

if pet_activated:
    st.markdown(f"**Pet Construction Speed Bonus:** {speed_bonus_percent_pet}%")
else:
    st.markdown("Pet Construction Speed Bonus: N/A")

st.markdown("---")

st.heade
