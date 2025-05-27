import streamlit as st

# Page config (title and icon)
st.set_page_config(
    page_title="WoS Upgrade and Troops Calculator",
    page_icon="❄️",
    layout="centered"
)

# Header
st.title("WoS Upgrade and Troops Calculator")
st.markdown("---")
st.caption("Made with 🩷 by [ARW]RealPookiePollo🐥 State #2543")
st.markdown("---")

st.write("Choose a calculator below 😀")

# Navigation buttons using page links (Streamlit will auto-detect .py files in the /pages folder)
col1, col2 = st.columns(2)

with col1:
    st.page_link("pages/building_upgrade.py", label="Building Upgrade Calculator", icon="📈")
    st.page_link("pages/fire_crystals_requirements.py", label="🔥 Fire Crystal Cost")
    st.page_link("pages/hero_gear.py", label="🔵 Hero Gear [Coming soon...]")
    st.page_link("pages/svs.py", label="⚔️ State vs State Prep Phase [Coming soon...]")


with col2:
    st.page_link("pages/troops_calculator.py", label="Troops Training & Upgrade Calculator", icon="🪖")
    st.page_link("pages/building_upgrade.py", label="Coming soon...")
    st.page_link("pages/chief_gear.py", label="🔵 Chief Gear [Coming soon...]")
    st.page_link("pages/hoc.py", label="📅 Hall of Chief [Coming soon...]")


st.markdown(
    """
    <div style="text-align: center; margin-top: 2em;">
        <a href="https://en.tipeee.com/woscalculatorapp" target="_blank">
            <button style="
                background-color:#ff5e57;
                color:white;
                border:none;
                padding:0.75em 1.5em;
                border-radius:0.5em;
                font-size:1em;
                cursor:pointer;">
                ❤️ Support the App on Tipeee
            </button>
        </a>
    </div>
    """,
    unsafe_allow_html=True
)


st.markdown("---")
