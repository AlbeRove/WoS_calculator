import streamlit as st
import pandas as pd
from datetime import timedelta
import os

st.set_page_config(page_title="Troops Training & Promotion", page_icon="🪖")

st.title("📈 Building Upgrade Calculator")
st.markdown("Select if you want to train or upgrade troops, the fill the required fields and select how many troops you want to train/upgrade in total")

# --- First define what to do: train or upgrade ---
action = st.radio("Select Action", ["Train Troops", "Upgrade Troops"])

# Show parameters based on selected action
if action == "Train Troops":
    training_speed = st.slider("Training Speed", min_value=1, max_value=100, value=50)
    training_capacity = st.number_input("Training Capacity", min_value=1, value=10)
    if st.button("Start Training"):
        st.success(f"Training started with speed {training_speed} and capacity {training_capacity}")

elif action == "Upgrade Troops":
    upgrade_level = st.selectbox("Upgrade Level", ["Level 1", "Level 2", "Level 3"])
    upgrade_cost = st.number_input("Upgrade Cost", min_value=0, value=100)
    if st.button("Start Upgrade"):
        st.success(f"Upgrade to {upgrade_level} started with cost {upgrade_cost}")
