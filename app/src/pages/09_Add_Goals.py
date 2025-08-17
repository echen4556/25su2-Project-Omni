import logging
import streamlit as st
import requests
from modules.nav import SideBarLinks
from datetime import date, datetime

logger = logging.getLogger(__name__)
st.set_page_config(layout='wide')

API_BASE_URL = "http://web-api:4000"   # your API container URL
SideBarLinks()

# Ensure user is logged in
if 'username' not in st.session_state or 'profileID' not in st.session_state:
    st.error("Please log in to continue.")
    st.stop()

profile_id = st.session_state['profileID']

# Page title
st.title("➕ Add New Goal")
st.write("Set a goal to track your progress.")

# Input fields
title = st.text_input("Goal Title")
target_date = st.date_input("Target Date", min_value=date.today())
status = st.selectbox("Status", ["Planned", "In Progress", "Completed"])

if st.button("Save Goal", type="primary"):
    # Call the backend API to create the goal
    payload = {
        "description": title,   # previously "name"
        "gameID": 2,            # choose a valid gameID
        "profileID": 9,          # must match a valid profileID in your database
        "date": datetime.now().isoformat() 
    }
    try:
        response = requests.post(f"{API_BASE_URL}/goals", json=payload)
        response.raise_for_status()
        st.success(f"Goal '{title}' saved successfully!")
        st.switch_page("pages/08_View_Goals.py")
    except requests.exceptions.RequestException as e:
        logger.error(f"Error creating goal: {e}")
        st.error(f"Failed to save goal: {e}")

if st.button("⬅ Cancel"):
    st.switch_page("pages/08_View_Goals.py")
