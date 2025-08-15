import logging
logger = logging.getLogger(__name__)

import streamlit as st
import requests
from modules.nav import SideBarLinks

# -------------------------------
# Page setup
# -------------------------------
st.set_page_config(layout='wide')
SideBarLinks()

# Make sure the user is logged in
if 'username' not in st.session_state or 'profileID' not in st.session_state:
    st.error("Please log in to continue.")
    st.stop()

username = st.session_state['username']
profile_id = st.session_state['profileID']

API_BASE_URL = "http://web-api:4000"

# -------------------------------
# Fetch all player profiles
# -------------------------------
@st.cache_data
def get_all_players():
    try:
        resp = requests.get(f"{API_BASE_URL}/profile")
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.HTTPError as http_err:
        if resp.status_code == 404:
            st.warning("No players found. Showing example data.")
            return [
                {"username": "ExamplePlayer1", "isPremium": True},
                {"username": "ExamplePlayer2", "isPremium": False}
            ]
        st.error(f"Error fetching players: {http_err}")
        return []
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching players: {e}")
        return []

# -------------------------------
# Fetch games for current user
# -------------------------------
@st.cache_data
def get_user_games(profile_id):
    try:
        resp = requests.get(f"{API_BASE_URL}/profiles/{profile_id}/games")
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.HTTPError as http_err:
        if resp.status_code == 404:
            st.warning("No games found for this profile. Showing example data.")
            return [
                {"game_id": 1, "game_name": "Example Game A"},
                {"game_id": 2, "game_name": "Example Game B"}
            ]
        st.error(f"Error fetching games: {http_err}")
        return []
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching games: {e}")
        return []

# -------------------------------
# Page title
# -------------------------------
st.title("🎮 Select Players and Game to Compare")

# Fetch players and games
players = get_all_players()
games = get_user_games(profile_id)

if not players or not games:
    st.info("No players or games available to select.")
    st.stop()

# -------------------------------
# Dropdown options
# -------------------------------
player_options = {p['username']: p['isPremium'] for p in players}
game_options = {g['game_name']: g['game_id'] for g in games}

selected_game_name = st.selectbox("Select Game", list(game_options.keys()))
selected_game_id = game_options[selected_game_name]

player1_name = st.selectbox("Select Player 1", list(player_options.keys()))
player2_name = st.selectbox("Select Player 2", list(player_options.keys()))

player1_premium = player_options[player1_name]
player2_premium = player_options[player2_name]

st.divider()

# -------------------------------
# Compare button
# -------------------------------
if st.button("🔍 Compare Players", use_container_width=True):
    if player1_name == player2_name:
        st.warning("Please select two different players.")
    else:
        st.session_state['compare'] = {
            'player1_name': player1_name,
            'player2_name': player2_name,
            'game_id': selected_game_id,
            'game_name': selected_game_name,
            'show_maps_weapons': player1_premium and player2_premium
        }
     #   st.rerun()
        st.switch_page("pages/33_Compare_Players.py")

# -------------------------------
# Select New Players
# -------------------------------
if st.button("⬅ Back to Select Players", use_container_width=True):
    st.switch_page("pages/32_Select_Players.py")
