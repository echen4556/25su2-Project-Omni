import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
from datetime import date

st.set_page_config(layout='wide')
SideBarLinks()

st.title("➕ Set New Goal")
st.write("Define a measurable and time-bound goal.")

goal_text = st.text_input("Goal Description")
deadline = st.date_input("Deadline", min_value=date.today())
progress = st.slider("Current Progress (%)", 0, 100, 0)

if st.button("Save Goal", type="primary"):
    # TODO: Save to DB
    st.success(f"Goal '{goal_text}' saved successfully!")
    st.switch_page("pages/08_View_Goals.py")

if st.button("⬅ Cancel"):
    st.switch_page("pages/08_View_Goals.py")
