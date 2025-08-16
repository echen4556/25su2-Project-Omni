import logging
logger = logging.getLogger(__name__)

import streamlit as st
import requests
import pandas as pd
from modules.nav import SideBarLinks

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
# Cached API calls
# -------------------------------
@st.cache_data
def get_profile(username, game_name):
    """Fetch profile info for a username and game"""
    try:
        resp = requests.get(f"{API_BASE_URL}/profile")
        resp.raise_for_status()
        profiles = resp.json()
        profile = next((p for p in profiles if p['username'] == username), None)
        if not profile:
            return None

        profile_id = profile['profileID']

        # Get gameProfiles for this profile
        resp = requests.get(f"{API_BASE_URL}/profiles/{profile_id}/gameProfiles")
        resp.raise_for_status()
        game_profiles = resp.json()
        game_instance = next((g for g in game_profiles if g['game_name'] == game_name), None)
        if not game_instance:
            return None

        return {
            "username": username,
            "isPremium": profile.get('isPremium', False),
            "profile_id": profile_id,
            "game_id": game_instance['game_id']
        }

    except requests.exceptions.RequestException as e:
        st.error(f"Failed to fetch profile for {username}: {e}")
        return None

@st.cache_data
def get_player_stats(profile_id, game_id):
    """Fetch player stats for a specific profile/game"""
    try:
        resp = requests.get(f"{API_BASE_URL}/playerStats/{profile_id}/{game_id}")
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.RequestException:
        return {}

@st.cache_data
def get_maps(game_id, profile_id=None):
    """Fetch maps (general or player-specific)."""
    try:
        if profile_id:
            resp = requests.get(f"{API_BASE_URL}/maps/{game_id}/{profile_id}")
        else:
            resp = requests.get(f"{API_BASE_URL}/maps/{game_id}")
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.RequestException:
        return []

@st.cache_data
def get_weapons(game_id, profile_id=None):
    """Fetch weapons (general or player-specific)."""
    try:
        if profile_id:
            resp = requests.get(f"{API_BASE_URL}/weapons/{game_id}/{profile_id}")
        else:
            resp = requests.get(f"{API_BASE_URL}/weapons/{game_id}")
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.RequestException:
        return []

# -------------------------------
# Gather data for both players
# -------------------------------
player_data = {}
for pname in [player1_name, player2_name]:
    profile = get_profile(pname, game_name)
    if not profile:
        st.error(f"No profile found for {pname} in {game_name}")
        st.stop()

    stats = get_player_stats(profile['profile_id'], profile['game_id'])

    maps, weapons = ([], [])
    if profile['isPremium'] and show_maps_weapons:
        maps = get_maps(profile['game_id'], profile['profile_id'])
        weapons = get_weapons(profile['game_id'], profile['profile_id'])

    player_data[pname] = {
        "stats": stats,
        "isPremium": profile['isPremium'],
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
            stats_df = pd.DataFrame(
                list(pdata['stats'].items()),
                columns=["Stat", "Value"]
            )
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
