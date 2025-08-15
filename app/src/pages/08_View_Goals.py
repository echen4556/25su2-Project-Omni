import logging
import streamlit as st
import requests
import pandas as pd
from modules.nav import SideBarLinks

logger = logging.getLogger(__name__)
st.set_page_config(layout='wide')

API_BASE_URL = "http://host.docker.internal:4000" 
SideBarLinks()

# Ensure user is logged in
if 'username' not in st.session_state or 'profileID' not in st.session_state:
    st.error("Please log in to continue.")
    st.stop()

profile_id = st.session_state['profileID']

# Fetch goals from API
def get_goals(profile_id):
    try:
        response = requests.get(f"{API_BASE_URL}/goals/profile/{profile_id}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching goals: {e}")
        st.error(f"Failed to retrieve goals: {e}")
        return []

st.title("🎯 View Goals")
st.write(f"Goals for {st.session_state['username']}:")

goals = get_goals(profile_id)
if goals:
    df = pd.DataFrame(goals)
    st.table(df)
else:
    st.info("You have no goals yet!")

# Navigation buttons
if st.button("⬅ Back to Milestones/Goals"):
    st.switch_page("pages/10_Milestones_Goals.py")

if st.button("➕ Add New Goal"):
    st.switch_page("pages/09_Add_Goals.py")
