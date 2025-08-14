import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')
SideBarLinks()

st.title("🏆 View Milestones")
st.write("Here are your tracked milestones:")

# Dummy milestone data — replace with DB call later
milestones = [
]

st.table(milestones)

if st.button("⬅ Back to Home"):
    st.switch_page("Home.py")
