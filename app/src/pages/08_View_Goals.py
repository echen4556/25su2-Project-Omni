import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')
SideBarLinks()

st.title("🎯 View Goals")
st.write("Here are your current goals:")

# Dummy goals data — replace with DB call later
goals = [
]

st.table(goals)

if st.button("⬅ Back to Home"):
    st.switch_page("Home.py")
