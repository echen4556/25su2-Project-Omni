import streamlit as st
import requests
import pandas as pd
import logging

logger = logging.getLogger(__name__)

API_BASE_URL = 'http://api:4000'

# A helper function to fetch a list of games for the current user
def get_user_games(profile_id):
    try:
        response = requests.get(f"{API_BASE_URL}/profiles/{profile_id}/games")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching user games: {e}")
        st.error("Failed to retrieve your game list. Please check the backend API.")
        return []

# A helper function to fetch a list of weapons for a specific game
def get_game_weapons(game_id):
    try:
        response = requests.get(f"{API_BASE_URL}/weapons/{game_id}/")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching game weapons: {e}")
        st.error("Failed to retrieve weapon list. Please check the backend API.")
        return []

# A helper function to fetch player statistics for a specific weapon in a specific game
def get_weapon_stats(profile_id, game_id, weapon_id):
    try:
        response = requests.get(f"{API_BASE_URL}/playerstats/{profile_id}/{game_id}/{weapon_id}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching weapon stats: {e}")
        st.error(f"Failed to retrieve weapon stats for ID: {weapon_id}. Please check the backend API.")
        return {}


# Page layout setup
st.set_page_config(layout='wide')

# Check if user is authenticated and get their profile ID
if 'authenticated' not in st.session_state or not st.session_state['authenticated']:
    st.error("You must be logged in to view this page.")
    st.stop()

# Retrieve the user's profile ID and premium status from the session state
profile_id = st.session_state.get('first_name')
is_premium = st.session_state.get('isPremium', False)

# Restrict access to premium users only
if not is_premium:
    st.error("Access Denied. This feature is for premium users only.")
    st.stop()

# Title of the page
st.title("🔫 Weapon Analytics")
st.write("View detailed statistics on your weapon performance from any game.")

# Fetch the list of games to populate the selectbox
games = get_user_games(profile_id)
game_names = [game.get('game_name') for game in games if 'game_name' in game]
game_ids = {game.get('game_name'): game.get('game_id') for game in games if 'game_name' in game}

if not games:
    st.warning("No games found for this user.")
else:
    # Create a dropdown to select a game
    selected_game_name = st.selectbox("Select a game:", game_names)
    selected_game_id = game_ids.get(selected_game_name)

    if selected_game_id:
        # Fetch the list of weapons for the selected game
        weapons = get_game_weapons(selected_game_id)
        weapon_names = [weapon.get('weapon_name') for weapon in weapons if 'weapon_name' in weapon]
        weapon_ids = {weapon.get('weapon_name'): weapon.get('weapon_id') for weapon in weapons if 'weapon_name' in weapon}

        if not weapons:
            st.info("No weapons found for this game.")
        else:
            # Create a dropdown to select a weapon
            selected_weapon_name = st.selectbox("Select a weapon:", weapon_names)
            selected_weapon_id = weapon_ids.get(selected_weapon_name)

            if selected_weapon_id:
                st.write("---")
                st.subheader(f"Stats for {selected_weapon_name} in {selected_game_name}")

                # Fetch and display the weapon stats for the selected player and weapon
                stats_data = get_weapon_stats(profile_id, selected_game_id, selected_weapon_id)
                if stats_data:
                    # Display stats in a clear, easy-to-read table format
                    stats_df = pd.DataFrame([stats_data])
                    stats_df = stats_df.transpose().reset_index()
                    stats_df.columns = ['Metric', 'Value']
                    st.table(stats_df)
                else:
                    st.info("No statistics available for this weapon.")
