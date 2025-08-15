import logging
logger = logging.getLogger(__name__)

import streamlit as st
import requests
from modules.nav import SideBarLinks

# Page setup
st.set_page_config(layout='wide')

# Show sidebar
SideBarLinks()

# Make sure the user is logged in
if 'username' not in st.session_state or 'profileID' not in st.session_state:
    st.error("Please log in to continue.")
    st.stop()

username = st.session_state['username']
profile_id = st.session_state['profileID']

@st.cache_data
def get_user_goals(profile_id):
    """Fetch goals for the given profile ID."""
    try:
        # TODO: Replace with actual API endpoint
        resp = requests.get(f"http://web-api:4000/goals/profile/{profile_id}")
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.HTTPError as http_err:
        if resp.status_code == 404:
            st.warning("No goals found for this profile. Showing example data.")
            return [
                {"id": 1, "goal": "Reach Diamond Rank", "target_date": "2025-09-01"},
                {"id": 2, "goal": "100 Headshots", "target_date": "2025-09-15"}
            ]
        st.error(f"Error fetching goals: {http_err}")
        return []
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching goals: {e}")
        return []

# Title
st.title("🎯 View Goals")
st.write(f"Here are your current goals for {username}:")

# Fetch goals
goals_list = get_user_goals(profile_id)

if goals_list:
    st.table(goals_list)
else:
    st.info("You don't have any goals yet.")

st.divider()

if st.button("⬅ Back to Home", use_container_width=True):
    st.switch_page("Home.py")
