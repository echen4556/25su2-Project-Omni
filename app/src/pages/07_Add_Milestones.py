import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
from datetime import date

st.set_page_config(layout='wide')
SideBarLinks()

st.title("➕ Add New Milestone")
st.write("Record a major achievement or planned objective.")

title = st.text_input("Milestone Title")
target_date = st.date_input("Target Date", min_value=date.today())
status = st.selectbox("Status", ["Planned", "In Progress", "Completed"])

if st.button("Save Milestone", type="primary"):
    # TODO: Save to DB
    st.success(f"Milestone '{title}' saved successfully!")
    st.switch_page("pages/06_View_Milestones.py")

if st.button("⬅ Cancel"):
    st.switch_page("pages/06_View_Milestones.py")
