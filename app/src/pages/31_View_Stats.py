import streamlit as st
import pandas as pd
import requests
import logging
from modules.nav import SideBarLinks # Assuming this is your navigation module

# --- Configuration ---
st.set_page_config(layout="wide")
logger = logging.getLogger(__name__)
API_BASE_URL = "http://api:4000"

# --- Page Setup ---
# Show sidebar links from your navigation module
SideBarLinks()

# Get user info and game info from session state
# This is now the definitive method for your Streamlit version
if 'profileID' not in st.session_state or \
   'selected_game_id' not in st.session_state or \
   'selected_game_name' not in st.session_state or \
   'viewing_profile_name' not in st.session_state or \
   'isPremium' not in st.session_state:
    st.error("Could not load game stats. Please navigate from the homepage.")
    st.stop()

# Get premium status from session
is_premium = st.session_state.get('isPremium')
st.write(is_premium)

# Get all required info from the session state
profile_id = st.session_state['profileID']
selected_game_id = st.session_state['selected_game_id']
selected_game_name = st.session_state['selected_game_name']
username = st.session_state['viewing_profile_name']


st.title(f"{selected_game_name} Statistics")
st.write(f"Viewing stats for **{username}**")
st.divider()

# --- Data Fetching Functions ---
# These functions call your Flask API. Add error handling for production.

@st.cache_data
def get_summary_stats(profile_id, game_id):
    """Fetches summary stats for a player in a specific game."""
    try:
        response = requests.get(f"{API_BASE_URL}/playerstats/summary/{profile_id}/{game_id}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return None # Return None if stats don't exist (404) or other error

@st.cache_data
def get_all_weapon_stats(profile_id, game_id):
    """Fetches all weapon stats for a player in a game."""
    try:
        # MOCKING API CALL FOR DEMONSTRATION
        weapon_stats = [
            {'statTableID': 1, 'weaponID': 101, 'name': 'Vandal', 'totalUsageTime': 12.5, 'kills': 150, 'accuracy': 0.25, 'amountBought': 200},
            {'statTableID': 1, 'weaponID': 102, 'name': 'Phantom', 'totalUsageTime': 8.2, 'kills': 95, 'accuracy': 0.35, 'amountBought': 150},
            {'statTableID': 1, 'weaponID': 103, 'name': 'Operator', 'totalUsageTime': 5.1, 'kills': 60, 'accuracy': 0.75, 'amountBought': 50},
        ]
        return pd.DataFrame(weapon_stats)
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching weapon stats: {e}")
        return pd.DataFrame()

@st.cache_data
def get_all_map_stats(profile_id, game_id):
    """Fetches all map stats for a player in a game."""
    try:
        # MOCKING API CALL FOR DEMONSTRATION
        map_stats = [
            {'statTableID': 1, 'mapID': 201, 'name': 'Ascent', 'kills': 200, 'wins': 50, 'losses': 30},
            {'statTableID': 1, 'mapID': 202, 'name': 'Bind', 'kills': 150, 'wins': 40, 'losses': 45},
            {'statTableID': 1, 'mapID': 203, 'name': 'Haven', 'kills': 100, 'wins': 30, 'losses': 20},
        ]
        return pd.DataFrame(map_stats)
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching map stats: {e}")
        return pd.DataFrame()

@st.cache_data
def get_all_weapon_stats(profile_id, game_id):
    """Fetches all weapon stats for a player in a game."""
    try:
        # This now makes a live API call
        response = requests.get(f"{API_BASE_URL}/playerstats/weapon/{profile_id}/{game_id}")
        response.raise_for_status()
        weapon_stats_data = response.json()
        # Convert the JSON response to a pandas DataFrame
        return pd.DataFrame(weapon_stats_data)
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching weapon stats: {e}")
        return pd.DataFrame()

@st.cache_data
def get_all_map_stats(profile_id, game_id):
    """Fetches all map stats for a player in a game."""
    try:
        # This now makes a live API call
        response = requests.get(f"{API_BASE_URL}/playerstats/map/{profile_id}/{game_id}")
        response.raise_for_status()
        map_stats_data = response.json()
        # Convert the JSON response to a pandas DataFrame
        return pd.DataFrame(map_stats_data)
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching map stats: {e}")
        return pd.DataFrame()


# --- UI Display ---

# Fetch all data for the selected game
summary_stats = get_summary_stats(profile_id, selected_game_id)
weapon_stats_df = get_all_weapon_stats(profile_id, selected_game_id)
map_stats_df = get_all_map_stats(profile_id, selected_game_id)

if not summary_stats:
    st.info(f"No stats found for **{selected_game_name}**. Play a match to see your stats here!")
else:
    # Display Summary Stats
    st.subheader("Overall Performance")
    kda = (summary_stats.get('kills', 0) + summary_stats.get('assists', 0)) / max(1, summary_stats.get('deaths', 1))

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Kills", summary_stats.get('kills', 0))
    col2.metric("Deaths", summary_stats.get('deaths', 0))
    col3.metric("Assists", summary_stats.get('assists', 0))
    col4.metric("KDA Ratio", f"{kda:.2f}")

    st.divider()

    # Display Weapon and Map Stats side-by-side
    col_w, col_m = st.columns(2)

    with col_w:
        st.subheader("Weapon Performance")
        if is_premium:
            if not weapon_stats_df.empty:
                # Ensure the necessary columns exist before trying to sort or display
                if 'totalUsageTime' in weapon_stats_df.columns:
                    sorted_weapons = weapon_stats_df.sort_values(by="totalUsageTime", ascending=False)
                    for index, row in sorted_weapons.iterrows():
                        with st.expander(f"**{row.get('name', 'Unknown Weapon')}**"):
                            st.metric("Kills with Weapon", row.get('kills', 0))
                            st.metric("Accuracy", f"{row.get('accuracy', 0):.1%}")
                            st.metric("Total Usage (Hours)", f"{row.get('totalUsageTime', 0):.2f}")
                else:
                    st.info("Weapon stats data is missing required columns.")
            else:
                st.info("No weapon stats available.")
        else:
            st.info("Upgrade to Premium to unlock detailed weapon stats.")
            if st.button("💎 Upgrade Now", key="weapon_upgrade", use_container_width=True):
                st.switch_page("pages/34_Premium_Upgrade.py")

    with col_m:
        st.subheader("Map Performance")
        if is_premium:
            if not map_stats_df.empty:
                # Ensure the necessary columns exist before calculations
                if 'wins' in map_stats_df.columns and 'losses' in map_stats_df.columns:
                    map_stats_df['totalMatches'] = map_stats_df['wins'] + map_stats_df['losses']
                    sorted_maps = map_stats_df.sort_values(by="totalMatches", ascending=False)
                    for index, row in sorted_maps.iterrows():
                        with st.expander(f"**{row.get('name', 'Unknown Map')}**"):
                            win_rate = row['wins'] / max(1, row['totalMatches'])
                            st.metric("Win Rate", f"{win_rate:.1%}")
                            st.metric("Total Wins", row.get('wins', 0))
                            st.metric("Total Losses", row.get('losses', 0))
                else:
                    st.info("Map stats data is missing required columns.")
            else:
                st.info("No map stats available.")
        else:
            st.info("Upgrade to Premium to unlock detailed map stats.")
            if st.button("💎 Upgrade Now", key="map_upgrade", use_container_width=True):
                st.switch_page("pages/34_Premium_Upgrade.py")

if st.button("⬅️ Back to Profile", use_container_width=True):
    # This assumes the homepage path was stored in session_state during login
    st.switch_page('pages/03_Emma_Smith_home.py')
