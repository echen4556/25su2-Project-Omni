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

if 'username' not in st.session_state or 'profileID' not in st.session_state:
    st.error("Please log in to continue.")
    st.stop()

API_BASE_URL = "http://host.docker.internal:4000"  # Docker desktop host
username = st.session_state['username']
profile_id = st.session_state['profileID']

# -------------------------------
# Fetch all player profiles
# -------------------------------
@st.cache_data
def get_all_players():
    try:
        resp = requests.get(f"{API_BASE_URL}/profiles")
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching players: {e}")
        return []

# -------------------------------
# Fetch games for a specific player
# -------------------------------
@st.cache_data
def get_user_games(profile_id):
    try:
        resp = requests.get(f"{API_BASE_URL}/profiles/{profile_id}/games")
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching games: {e}")
        return []

# -------------------------------
# Page title
# -------------------------------
st.title("🎮 Compare Players by Common Games")

# Fetch players
players = get_all_players()
if not players:
    st.info("No players available.")
    st.stop()

# Build a map of username -> (profileID, isPremium)
player_map = {p['username']: (p['profileID'], p['isPremium']) for p in players}

# -------------------------------
# Player selection dropdowns
# -------------------------------
def select_player(label):
    options = [(username, pid, premium) for username, (pid, premium) in player_map.items()]
    selected = st.selectbox(
        label,
        options,
        format_func=lambda x: x[0]  # only show username
    )
    return selected[0], selected[1], selected[2]

player1_name, player1_id, player1_premium = select_player("Select Player 1")
player2_name, player2_id, player2_premium = select_player("Select Player 2")

if player1_id == player2_id:
    st.warning("Please select two different players.")
else:
    # -------------------------------
    # Fetch and map player games
    # -------------------------------
    player1_games = get_user_games(player1_id)
    player2_games = get_user_games(player2_id)

    p1_game_map = {g['gameID']: g for g in player1_games}
    p2_game_map = {g['gameID']: g for g in player2_games}

    # Find common games
    common_game_ids = set(p1_game_map.keys()) & set(p2_game_map.keys())

    if common_game_ids:
        # Build list of tuples: (game_name, gameID)
        common_games_list = [(p1_game_map[gid]['name'], gid) for gid in common_game_ids]

        # Selectbox for common games
        selected_game_name, selected_game_id = st.selectbox(
            "Select Common Game",
            common_games_list,
            format_func=lambda x: x[0]
        )

        # Compare button
        if st.button("🔍 Compare Players", use_container_width=True):
            st.session_state['compare'] = {
                'player1_name': player1_name,
                'player2_name': player2_name,
                'game_id': selected_game_id,
                'game_name': selected_game_name,
                'show_maps_weapons': player1_premium and player2_premium
            }
            st.switch_page("pages/33_Compare_Players.py")
    else:
        st.info("❌ These two players don’t share any games in common.")

# -------------------------------
# Back button
# -------------------------------
if st.button("⬅ Back to Home", use_container_width=True):
    st.switch_page("pages/Home.py")
