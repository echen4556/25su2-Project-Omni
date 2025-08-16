import streamlit as st
import requests
import pandas as pd
from modules.nav import SideBarLinks

# --- Page config ---
st.set_page_config(layout='wide')
SideBarLinks()

# --- Check login and session state ---
if 'username' not in st.session_state or 'profileID' not in st.session_state:
    st.error("Please log in to continue.")
    st.stop()

profile_id = st.session_state['profileID']

# Use the correct service name for Docker networking
API_BASE_URL = "http://api:4000"

@st.cache_data
def fetch_match_history(profile_id):
    """Fetches all match history for a user in a specific game."""
    try:
        # Call the new, efficient endpoint
        url = f"{API_BASE_URL}/matches/profile/{profile_id}"
        r = requests.get(url)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        st.error(f"Error fetching match history: {e}")
        return []

# --- Display ---
st.title(f"Match History")
matches = fetch_match_history(profile_id)

if not matches:
    st.info("No matches found for this game.")
else:
    for match in matches:
        # Format the win/loss status for better display
        result = "Victory" if match.get('win') else "Defeat"

        st.subheader(f"{match.get('gameName')} Map: {match.get('mapName', 'Unknown')} - {result}")
        st.write(f"**Match ID:** {match.get('matchID')} | **Date:** {match.get('matchDate', 'Unknown')}")

        # Use columns for a cleaner layout
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Kills", match.get('kills', 0))
        col2.metric("Deaths", match.get('deaths', 0))
        col3.metric("Assists", match.get('assists', 0))
        col4.metric("Headshots", match.get('headshots', 0))

        st.write(f"**Damage Dealt:** {match.get('damage', 0)}")
        st.write(f"**Match Type:** {match.get('matchType', 'N/A')} | **Lobby Rank:** {match.get('lobbyRank', 'N/A')}")

        st.divider()
