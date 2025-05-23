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

# Show inputs if any action was selected
# Show inputs in two columns
if st.session_state.action in ["train", "upgrade"]:
    st.subheader(f"{st.session_state.action.capitalize()} Parameters")

    param_col1, param_col2 = st.columns(2)

    with param_col1:
        training_speed = st.slider("Training Speed", min_value=1, max_value=100, value=50)

    with param_col2:
        training_capacity = st.number_input("Training Capacity", min_value=1, value=10)
