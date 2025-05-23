import streamlit as st
import pandas as pd
from datetime import timedelta
import os

st.set_page_config(page_title="Troops Training & Promotion", page_icon="🪖")

st.title("Troops Training & Promotion")
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

    param_col1, param_col2 = st.columns(2)
    with param_col1:
        training_speed_input = st.text_input("Training Speed", value="10")
    with param_col2:
        training_capacity_input = st.text_input("Training Capacity", value="100")
    capacity_bonus = st.checkbox("3x Capacity city bonus", value=False)
    # Validate inputs
    try:
        training_speed = float(training_speed_input)
        training_capacity = int(training_capacity_input)
        if capacity_bonus: 
            training_capacity = training_capacity * 3 
        
        st.success(f"""Success""")
    except ValueError:
        st.error("Please enter valid values for both speed and capacity.")

st.title("Select Troops")

# Troop types and icons
troops = {
    "Infantry": "🛡️",
    "Lancers": "🗡️",
    "Marksmen": "🏹"
}

# Initialize toggle states
for troop in troops:
    if f"toggle_{troop}" not in st.session_state:
        st.session_state[f"toggle_{troop}"] = False

# Display toggles in 3 columns
cols = st.columns(3)
for i, (troop, icon) in enumerate(troops.items()):
    with cols[i % 3]:
        st.session_state[f"toggle_{troop}"] = st.toggle(
            f"{icon} {troop}", value=st.session_state[f"toggle_{troop}"]
        )

# Get selected troops
selected_troops = [troop for troop in troops if st.session_state[f"toggle_{troop}"]]

# Show result
if selected_troops:
    st.success("Selected troops to train: " + ", ".join(selected_troops))
else:
    st.info("No troop type selected.")

# For each selected troop, show level and number input fields
troop_params = {}

for troop in troops:
    if st.session_state.get(f"toggle_{troop}", False):
        st.subheader(f"{troops[troop]} {troop} Parameters")
        
        # Create two columns for neat layout
        col_level, col_number = st.columns(2)
        
        with col_level:
            level = st.selectbox(
                f"{troop} Level", options=list(range(1, 12)), key=f"{troop}_level"
            )
        with col_number:
            number = st.number_input(
                f"Number of {troop}", min_value=0, step=1, key=f"{troop}_number"
            )
        
        troop_params[troop] = {"level": level, "number": number}

# Load CSVs into a dict keyed by troop name (lowercase)
troop_data = {}
for troop in ["infantry", "lancer", "marksman"]:
    file_path = os.path.join(data_path, f"data/{troop}.csv")
    if os.path.exists(file_path):
        troop_data[troop] = pd.read_csv(file_path)
    else:
        st.warning(f"File {file_path} not found!")

