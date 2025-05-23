import streamlit as st

# Page config (title and icon)
st.set_page_config(
    page_title="WoS Upgrade and Troops Calculator",
    page_icon="🎮",
    layout="centered"
)

# Header
st.title("WoS Upgrade and Troops Calculator")
st.subheader("Powered by [ARW]Pollo🐥 State #2543")
st.write("Choose a calculator below 😀")

# Navigation buttons using page links (Streamlit will auto-detect .py files in the /pages folder)
col1, col2 = st.columns(2)

with col1:
    st.page_link("pages/building_upgrade.py", label="Buildinf Upgrade Calculator", icon="📈")
    st.page_link("pages/troops_calculator.py", label="[⚠️WORK IN PROGRESS⚠️]", icon="🪖")

with col2:
    st.page_link("pages/building_upgrade.py", label="Coming soon...")
    st.page_link("pages/building_upgrade.py", label="Coming soon...")

st.markdown("---")
st.caption("Made with ❤️ using Streamlit")

