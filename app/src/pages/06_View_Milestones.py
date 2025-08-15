import logging
import streamlit as st
import requests
import pandas as pd
from modules.nav import SideBarLinks

logger = logging.getLogger(__name__)
API_BASE_URL = "http://host.docker.internal:4000" 

st.set_page_config(layout='wide')
SideBarLinks()

# Ensure user is logged in
if 'username' not in st.session_state or 'profileID' not in st.session_state:
    st.error("Please log in to continue.")
    st.stop()

profile_id = st.session_state['profileID']

st.title("🏆 View Milestones")
st.write("Here are your tracked milestones:")

# Fetch milestones from API
try:
    r = requests.get(f"{API_BASE_URL}/milestones/profile/{profile_id}")
    r.raise_for_status()
    milestones = r.json()
except requests.exceptions.RequestException as e:
    st.error(f"Error fetching milestones: {e}")
    milestones = []

if milestones:
    df = pd.DataFrame(milestones)
    st.table(df)
else:
    st.info("You have no milestones yet.")

if st.button("⬅ Back to Home"):
    st.switch_page("Home.py")
