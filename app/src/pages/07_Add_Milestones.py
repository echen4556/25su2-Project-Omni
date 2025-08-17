import logging
import streamlit as st
import requests
from datetime import date
from modules.nav import SideBarLinks

logger = logging.getLogger(__name__)
API_BASE_URL = "http://web-api:4000"

st.set_page_config(layout='wide')
SideBarLinks()

# Ensure user is logged in
if 'username' not in st.session_state or 'profileID' not in st.session_state:
    st.error("Please log in to continue.")
    st.stop()

profile_id = st.session_state["profileID"]

st.title("➕ Add New Milestone")
st.write("Record a major achievement or planned objective.")

title = st.text_input("Milestone Title")
target_date = st.date_input("Target Date", min_value=date.today())
status = st.selectbox("Status", ["Planned", "In Progress", "Completed"])

if st.button("Save Milestone", type="primary"):
    payload = {
        "profile_id": profile_id,
        "title": title,
        "target_date": target_date.isoformat(),
        "status": status
    }
    try:
        r = requests.post(f"{API_BASE_URL}/milestones", json=payload)
        r.raise_for_status()
        st.success(f"Milestone '{title}' saved successfully!")
        st.switch_page("pages/06_View_Milestones.py")
    except requests.exceptions.RequestException as e:
        st.error(f"Error saving milestone: {e}")

if st.button("⬅ Cancel"):
    st.switch_page("pages/06_View_Milestones.py")
