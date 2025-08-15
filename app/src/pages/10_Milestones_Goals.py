import logging
logger = logging.getLogger(__name__)

import streamlit as st
import requests
from modules.nav import SideBarLinks

# ----------------- Page Setup -----------------
st.set_page_config(layout='wide')
SideBarLinks()

# ----------------- Authentication Check -----------------
if 'profileID' not in st.session_state or 'username' not in st.session_state:
    st.error("Please log in first.")
    st.stop()

profile_id = st.session_state['profileID']
username = st.session_state['username']

# ----------------- API Setup -----------------
API_BASE_URL = "http://host.docker.internal:4000"   # adjust if needed

@st.cache_data
def get_milestones(profile_id):
    """Fetch milestones for the given profile from the API."""
    try:
        r = requests.get(f"{API_BASE_URL}/milestones/profile/{profile_id}")
        r.raise_for_status()
        return r.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching milestones: {e}")
        return []

@st.cache_data
def get_goals(profile_id):
    """Fetch goals for the given profile from the API."""
    try:
        r = requests.get(f"{API_BASE_URL}/goals/profile/{profile_id}")
        r.raise_for_status()
        return r.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching goals: {e}")
        return []

# ----------------- Page Content -----------------
st.title(f"{username}'s Milestones & Goals")
st.write("Track your achievements and set actionable objectives to improve performance.")
st.write("")

# ----------------- Milestones -----------------
st.subheader("🏆 Milestones")
milestones = get_milestones(profile_id)

col1, col2 = st.columns(2)
with col1:
    if st.button("🎯 View All Milestones"):
        st.switch_page("pages/06_View_Milestones.py")
with col2:
    if st.button("➕ Add New Milestone"):
        st.switch_page("pages/07_Add_Milestones.py")

st.write("---")  # Separator

# ----------------- Goals -----------------
st.subheader("🎯 Goals")
goals = get_goals(profile_id)

col1, col2 = st.columns(2)
with col1:
    if st.button("📋 View Current Goals"):
        st.switch_page("pages/08_View_Goals.py")
with col2:
    if st.button("➕ Set New Goal"):
        st.switch_page("pages/09_Add_Goals.py")
