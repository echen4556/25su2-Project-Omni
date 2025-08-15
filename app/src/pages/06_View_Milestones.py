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
def get_user_milestones(profile_id):
    """Fetch milestones for the given profile ID."""
    try:
        # TODO: Replace with actual API endpoint
        resp = requests.get(f"http://web-api:4000/milestones/profile/{profile_id}")
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.HTTPError as http_err:
        if resp.status_code == 404:
            st.warning("No milestones found for this profile. Showing example data.")
            return [
                {"id": 1, "name": "First Win", "date": "2025-08-01"},
                {"id": 2, "name": "100 Kills", "date": "2025-08-05"}
            ]
        st.error(f"Error fetching milestones: {http_err}")
        return []
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching milestones: {e}")
        return []

# Title
st.title("🏆 View Milestones")
st.write(f"Here are your tracked milestones for {username}:")

# Fetch milestones
milestones_list = get_user_milestones(profile_id)

if milestones_list:
    st.table(milestones_list)
else:
    st.info("You don't have any milestones yet.")

st.divider()

if st.button("⬅ Back to Home", use_container_width=True):
    st.switch_page("Home.py")
