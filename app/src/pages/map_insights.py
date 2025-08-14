import streamlit as st
import requests
import pandas as pd
import logging

# Set up basic logging for this page
logger = logging.getLogger(__name__)

# The base URL for your Flask API.
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

# A helper function to fetch a list of maps for a specific game
def get_game_maps(game_id):
    try:
        response = requests.get(f"{API_BASE_URL}/map/{game_id}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching game maps: {e}")
        st.error("Failed to retrieve map list. Please check the backend API.")
        return []

# A helper function to fetch player statistics for a specific map in a specific game
def get_map_stats(profile_id, game_id, map_id):
    try:
        response = requests.get(f"{API_BASE_URL}/playerstats/map/{profile_id}/{game_id}/{map_id}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching map stats: {e}")
        st.error(f"Failed to retrieve map stats for ID: {map_id}. Please check the backend API.")
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
st.title("🗺️ Map Insights")
st.write("View detailed statistics and insights on your map performance.")

# Fetch the list of games to populate the selectbox
games = get_user_games(profile_id)
game_names = [game.get('name') for game in games if 'name' in game]
game_ids = {game.get('name'): game.get('gameID') for game in games if 'name' in game}

if not games:
    st.warning("No games found for this user.")
else:
    # Create a dropdown to select a game
    selected_game_name = st.selectbox("Select a game:", game_names)
    selected_game_id = game_ids.get(selected_game_name)

    if selected_game_id:
        maps = get_game_maps(selected_game_id)
        map_names = [m.get('name') for m in maps if 'name' in m]
        map_ids = {m.get('name'): m.get('mapID') for m in maps if 'name' in m}
        if not maps:
            st.info("No maps found for this game.")
        else:
            selected_map_name = st.selectbox("Select a map:", map_names)
            selected_map_id = map_ids.get(selected_map_name)

            if selected_map_id:
                st.write("---")
                st.subheader(f"Insights for {selected_map_name} in {selected_game_name}")

                # Fetch and display the map stats for the selected player and map
                stats_data = get_map_stats(profile_id, selected_game_id, selected_map_id)
                if stats_data:
                    stats_df = pd.DataFrame([stats_data])
                    stats_df = stats_df.transpose().reset_index()
                    stats_df.columns = ['Metric', 'Value']
                    st.table(stats_df)
                else:
                    st.info("No statistics available for this map.")
