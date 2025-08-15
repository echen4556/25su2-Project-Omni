import streamlit as st
import requests
from modules.nav import SideBarLinks

# --- Page config ---
st.set_page_config(layout='wide')
SideBarLinks()

# --- Check login ---
if 'username' not in st.session_state or 'profileID' not in st.session_state:
    st.error("Please log in to continue.")
    st.stop()

# --- Check if match history info exists ---
if 'selected_profile_id' not in st.session_state:
    st.error("No game selected. Go back and pick a game.")
    st.stop()

profile_id = st.session_state.selected_profile_id
game_instance_id = st.session_state.selected_game_instance_id
game_name = st.session_state.selected_game_name

API_BASE_URL = "http://host.docker.internal:4000"

@st.cache_data
def fetch_all_matches(profile_id, game_instance_id):
    try:
        url = f"{API_BASE_URL}/profile/{profile_id}/games/{game_instance_id}/matches"
        r = requests.get(url)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        st.error(f"Error fetching matches: {e}")
        return []

@st.cache_data
def fetch_match_details(match_id):
    try:
        url = f"{API_BASE_URL}/matches/{match_id}/{profile_id}"
        r = requests.get(url)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        st.error(f"Error fetching match {match_id} details: {e}")
        return {}

# --- Display ---
st.title(f"Match History - {game_name}")
matches = fetch_all_matches(profile_id, game_instance_id)

if not matches:
    st.info("No matches found for this game.")
else:
    for match in matches:
        match_id = match.get("matchID")
        st.subheader(f"Match ID: {match_id} | Date: {match.get('matchDate', 'Unknown')}")
        st.write(f"Match Type: {match.get('matchType', 'N/A')}")
        st.write(f"Lobby Rank: {match.get('lobbyRank', 'N/A')}")
        st.write(f"Map: {match.get('mapName', 'Unknown')}")

        details = fetch_match_details(match_id)
        if details:
            st.write(f"Kills: {details.get('kills', 0)} | Deaths: {details.get('deaths', 0)} | Assists: {details.get('assists', 0)}")
            st.write(f"Headshots: {details.get('headshots', 0)} | Total Damage: {details.get('damage', 0)}")
            st.write(f"Rounds: {details.get('rounds', 0)} | Match Duration: {details.get('matchDuration', 0)} seconds")
        st.divider()
