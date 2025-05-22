import streamlit as st

# Page config (title and icon)
st.set_page_config(
    page_title="Game Calculator Hub",
    page_icon="🎮",
    layout="centered"
)

# Header
st.title("🎮 Game Calculator Hub")
st.subheader("Welcome, adventurer!")
st.write("Choose a calculator below to optimize your game strategy:")

# Navigation buttons using page links (Streamlit will auto-detect .py files in the /pages folder)
col1, col2 = st.columns(2)

with col1:
    st.page_link("pages/building_upgrade.py", label="Upgrade Cost Calculator", icon="📈")
    st.page_link("pages/building_upgrade.py", label="Coming soon...")

with col2:
    st.page_link("pages/building_upgrade.py", label="Coming soon...")
    st.page_link("pages/building_upgrade.py", label="Coming soon...")

st.markdown("---")
st.caption("Made with ❤️ using Streamlit")

