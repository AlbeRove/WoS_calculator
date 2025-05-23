import streamlit as st
import pandas as pd
from datetime import timedelta
import os

st.set_page_config(page_title="Troops Training & Promotion", page_icon="🪖")

st.title("Troops Training & Promotion")
st.markdown("Select if you want to train or upgrade troops, the fill the required fields and select how many troops you want to train/upgrade in total")

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

base_train_time ={1:   12, 
                  2:   17,
                  3:   24,
                  4:   32,
                  5:   44,
                  6:   60,
                  7:   83,
                  8:  113,
                  9:  131,
                  10: 152,
                  11: 180}


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

        col1, col2, col3 = st.columns(3)
        if st.session_state.action == "train":
            with col1:
                level = st.selectbox(
                    f"{troop} Level", options=list(range(1, 12)), key=f"{troop}_level"
                )
        elif st.session_state.action == "upgrade":
            with col1:
                start_level = st.selectbox(
                    f"{troop} Start Level", options=list(range(1, 11)), key=f"{troop}_start"
                )
            with col2:
                end_level = st.selectbox(
                    f"{troop} End Level", options=list(range(2, 12)), key=f"{troop}_end"
                )

        with col3:
            number = st.number_input(
                f"Number of {troop}", min_value=0, step=1, key=f"{troop}_number"
            )

        if st.session_state.action == "train":
            troop_params[troop] = {"level": level, "number": number}
        elif st.session_state.action == "upgrade":
            if start_level >= end_level:
                st.warning(f"End level must be greater than start level for {troop}")
            else:
                troop_params[troop] = {
                    "start_level": start_level,
                    "end_level": end_level,
                    "number": number
                }

# Load CSVs into a dict keyed by troop name (lowercase)
troop_data = {}
for troop in ["infantry", "lancer", "marksman"]:
    file_path = f"data/{troop}.csv"
    if os.path.exists(file_path):
        troop_data[troop] = pd.read_csv(file_path)
    else:
        st.warning(f"File {file_path} not found!")

if st.button("Calculate"):
    if not troop_params:
        st.warning("Select at least one troop and specify parameters.")
    else:
        total_resources = {"Meat": 0, "Wood": 0, "Coal": 0, "Iron": 0}
        total_base_time_sec = 0  # Total base training time in seconds
        troop_key_map = {"Infantry": "infantry", "Lancers": "lancer", "Marksmen": "marksman"}

        for troop, params in troop_params.items():
            troop_df = troop_data[troop_key_map[troop]]
if st.button("Calculate"):
    if not troop_params:
        st.warning("Select at least one troop and specify parameters.")
    else:
        total_resources = {"Meat": 0, "Wood": 0, "Coal": 0, "Iron": 0}
        total_base_time_sec = 0  # Total base training time in seconds
        troop_key_map = {"Infantry": "infantry", "Lancers": "lancer", "Marksmen": "marksman"}

        for troop, params in troop_params.items():
            troop_df = troop_data[troop_key_map[troop]]

            def parse_int(x):
                if isinstance(x, str):
                    return int(x.replace(",", ""))
                return int(x)

            if st.session_state.action == "train":
                level = params["level"]
                number = params["number"]

                row = troop_df[troop_df["Level"] == level]
                if row.empty:
                    st.error(f"Level {level} not found for {troop}")
                    continue
                row = row.iloc[0]

                meat_cost = parse_int(row["Meat"])
                wood_cost = parse_int(row["Wood"])
                coal_cost = parse_int(row["Coal"])
                iron_cost = parse_int(row["Iron"])

                total_resources["Meat"] += meat_cost * number
                total_resources["Wood"] += wood_cost * number
                total_resources["Coal"] += coal_cost * number
                total_resources["Iron"] += iron_cost * number

                base_time_per_troop = base_train_time[level]
                total_base_time_sec += base_time_per_troop * number

            elif st.session_state.action == "upgrade":
                start = params["start_level"]
                end = params["end_level"]
                number = params["number"]

                for lvl in range(start + 1, end + 1):
                    row_now = troop_df[troop_df["Level"] == lvl]
                    row_prev = troop_df[troop_df["Level"] == lvl - 1]

                    if row_now.empty or row_prev.empty:
                        st.error(f"Level data missing for level {lvl} or {lvl-1} in {troop}")
                        continue

                    row_now = row_now.iloc[0]
                    row_prev = row_prev.iloc[0]

                    meat_cost = parse_int(row_now["Meat"]) - parse_int(row_prev["Meat"])
                    wood_cost = parse_int(row_now["Wood"]) - parse_int(row_prev["Wood"])
                    coal_cost = parse_int(row_now["Coal"]) - parse_int(row_prev["Coal"])
                    iron_cost = parse_int(row_now["Iron"]) - parse_int(row_prev["Iron"])
                    time_cost = base_train_time[lvl] - base_train_time[lvl - 1]

                    total_resources["Meat"] += meat_cost * number
                    total_resources["Wood"] += wood_cost * number
                    total_resources["Coal"] += coal_cost * number
                    total_resources["Iron"] += iron_cost * number
                    total_base_time_sec += time_cost * number

        # Calculate reduced training time
        reduction_factor = 1 / (1 + training_speed / 100)
        total_reduced_time_sec = total_base_time_sec * reduction_factor

        # Format time
        def format_time(seconds):
            hours = int(seconds // 3600)
            minutes = int((seconds % 3600) // 60)
            secs = int(seconds % 60)
            return f"{hours}h {minutes}m {secs}s"

        # Display resource totals
        st.subheader("Total Resource Cost")
        total_df = pd.DataFrame(total_resources.items(), columns=["Resource", "Total Amount"])
        st.table(total_df)

        # Display training times
        st.subheader("Training Time")
        st.markdown(f"**Total Base Training Time:** {format_time(total_base_time_sec)}")
        st.markdown(f"**Reduced Training Time:** {format_time(total_reduced_time_sec)}")




