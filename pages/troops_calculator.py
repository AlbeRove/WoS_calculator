import streamlit as st
import pandas as pd
from datetime import timedelta
import os

st.set_page_config(page_title="Troops Training & Promotion", page_icon="🪖")

st.title("📈 Building Upgrade Calculator")
st.markdown("Select if you want to train or upgrade troops, the fill the required fields and select how many troops you want to train/upgrade in total")

# --- First define what to do: train or upgrade ---
# Create two columns for buttons
col1, col2 = st.columns(2)

# Use session state to track which button was clicked
if "action" not in st.session_state:
    st.session_state.action = None

# Define button actions
with col1:
    if st.button("Train Troops"):
        st.session_state.action = "train"
with col2:
    if st.button("Upgrade Troops"):
        st.session_state.action = "upgrade"

# Show inputs in two columns
if st.session_state.action in ["train", "upgrade"]:
    st.subheader(f"{st.session_state.action.capitalize()} Parameters")

    with param_col1:
        training_speed_input = st.text_input("Training Speed", value="10")
    with param_col2:
        training_capacity_input = st.text_input("Training Capacity", value="100")

    # Validate inputs
    try:
        training_speed = int(training_speed_input)
        training_capacity = int(training_capacity_input)
        st.success(f"Speed: {training_speed}, Capacity: {training_capacity}")
    except ValueError:
        st.error("Please enter valid integers for both speed and capacity.")
