import streamlit as st
import pandas as pd
import os

st.title("🔥 Fire Crystal Calculator")
st.markdown("Calculate how many Fire Crystals are needed to upgrade selected buildings.")

# Mapping of building names to their CSV filenames
BUILDINGS = {
    "Furnace": "furnace.csv",
    "Embassy": "embassy.csv",
    "Infirmary": "infirmary.csv",
    "Command Center": "commandcenter.csv",
    "Infantry Camp": "infantrycamp.csv",
    "Lancer Camp": "lancercamp.csv",
    "Marksman Camp": "marksmancamp.csv",
}

selected_buildings = {}

# Toggle and input for each building
for name, filename in BUILDINGS.items():
    with st.expander(name):
        use_building = st.toggle(f"Upgrade {name}")
        if use_building:
            col1, col2 = st.columns(2)
            with col1:
                start_level = st.number_input(f"{name} Start Level", min_value=30, max_value=54, key=f"{name}_start")
            with col2:
                end_level = st.number_input(f"{name} Target Level", min_value=31, max_value=55, key=f"{name}_end")
            selected_buildings[name] = (filename, start_level, end_level)

# Calculate button
if st.button("Calculate"):
    total_crystals = 0
    details = []
    for name, (filename, start, end) in selected_buildings.items():
        if start >= end:
            st.warning(f"{name}: Start level must be less than target level.")
            continue
        try:
            df = pd.read_csv(f"data/{filename}")
            df = df[(df['level'] > start) & (df['level'] <= end)]
            cost = df['firecrystals'].sum()
            total_crystals += cost
            details.append(f"🔹 {name}: {int(cost)} Fire Crystals")
        except Exception as e:
            st.error(f"Error loading {name} data: {e}")

    st.subheader("Fire Crystal Summary")
    st.write("\n".join(details))
    st.success(f"**Total Fire Crystals Required: {int(total_crystals)}**")

