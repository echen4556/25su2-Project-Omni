import logging
import streamlit as st
import requests
import pandas as pd
from modules.nav import SideBarLinks

logger = logging.getLogger(__name__)

# -------------------------------
# Page setup
# -------------------------------
st.set_page_config(layout='wide')
SideBarLinks()

API_BASE_URL = "http://host.docker.internal:4000"

# -------------------------------
# Ensure user is logged in
# -------------------------------
if 'username' not in st.session_state:
    st.error("You must be logged in to view this page.")
    st.stop()

# -------------------------------
# Ensure comparison data exists
# -------------------------------
if "compare" not in st.session_state:
    st.warning("No players selected to compare. Go back to selection page.")
    st.stop()

compare = st.session_state['compare']
player1_name = compare['player1_name']
player2_name = compare['player2_name']
game_name = compare['game_name']
show_maps_weapons = compare['show_maps_weapons']

# -------------------------------
# Cached API helpers
# -------------------------------
@st.cache_data
def get_profile_by_username(username: str):
    try:
        resp = requests.get(f"{API_BASE_URL}/profiles")
        resp.raise_for_status()
        profiles = resp.json()
        return next((p for p in profiles if p['username'] == username), None)
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching profile for {username}: {e}")
        return None

@st.cache_data
def get_game_profile(profile_id: int):
    try:
        resp = requests.get(f"{API_BASE_URL}/gamesProfiles/{profile_id}")
        resp.raise_for_status()
        game_profiles = resp.json()
        return game_profiles
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching game profile for profile {profile_id}: {e}")
        return None

@st.cache_data
def get_player_stats(profile_id: int, game_id: int):
    try:
        resp = requests.get(f"{API_BASE_URL}/playerStats/{profile_id}/{game_id}")
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.RequestException:
        return {}

@st.cache_data
def get_maps(game_id: int, profile_id: int = None):
    try:
        url = f"{API_BASE_URL}/maps/{game_id}/{profile_id}" if profile_id else f"{API_BASE_URL}/maps/{game_id}"
        resp = requests.get(url)
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.RequestException:
        return []

@st.cache_data
def get_weapons(game_id: int, profile_id: int = None):
    try:
        url = f"{API_BASE_URL}/weapons/{game_id}/{profile_id}" if profile_id else f"{API_BASE_URL}/weapons/{game_id}"
        resp = requests.get(url)
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.RequestException:
        return []

# -------------------------------
# Fetch data for both players
# -------------------------------
player_data = {}
for pname in [player1_name, player2_name]:
    profile = get_profile_by_username(pname)
    if not profile:
        st.error(f"No profile found for {pname}")
        st.stop()

    game_profile = get_game_profile(profile['profileID'])
    if not game_profile:
        st.error(f"{pname} does not have a profile for {game_name}")
        st.stop()

    stats = get_player_stats(profile['profileID'], game_profile)
    maps, weapons = [], []

    if profile.get('isPremium', False) and show_maps_weapons:
        maps = get_maps(game_profile['game_id'], profile['profileID'])
        weapons = get_weapons(game_profile['game_id'], profile['profileID'])

    player_data[pname] = {
        "stats": stats,
        "isPremium": profile.get('isPremium', False),
        "maps": maps,
        "weapons": weapons
    }

# -------------------------------
# Display comparison
# -------------------------------
st.title(f"📊 Comparing {player1_name} vs {player2_name}")
st.subheader(f"Game: {game_name}")

col1, col2 = st.columns(2)
for col, pname in zip([col1, col2], [player1_name, player2_name]):
    pdata = player_data[pname]
    with col:
        st.markdown(f"### {pname}")

        # Core stats
        if pdata['stats']:
            stats_df = pd.DataFrame(list(pdata['stats'].items()), columns=["Stat", "Value"])
            st.table(stats_df)
        else:
            st.info("No stats available.")

        # Premium maps & weapons
        if pdata['isPremium'] and show_maps_weapons:
            st.success("Premium: Maps & Weapons Stats")

            if pdata['maps']:
                st.write("**Maps:**")
                st.table(pd.DataFrame(pdata['maps']))
            else:
                st.write("No map data available.")

            if pdata['weapons']:
                st.write("**Weapons:**")
                st.table(pd.DataFrame(pdata['weapons']))
            else:
                st.write("No weapon data available.")
        else:
            st.info("Maps and weapons stats are hidden (premium only).")

# -------------------------------
# Back button
# -------------------------------
if st.button("⬅ Back to Player Selection", use_container_width=True):
    st.switch_page("pages/32_Select_Players.py")
