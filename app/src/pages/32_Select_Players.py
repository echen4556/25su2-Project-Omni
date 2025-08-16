import logging
import streamlit as st
import requests
from modules.nav import SideBarLinks

logger = logging.getLogger(__name__)

# -------------------------------
# Page setup
# -------------------------------
st.set_page_config(layout='wide')
SideBarLinks()

# Make sure the user is logged in
if 'username' not in st.session_state or 'profileID' not in st.session_state:
    st.error("Please log in to continue.")
    st.stop()

# CORRECTED: Use the service name 'api' for Docker networking
API_BASE_URL = "http://api:4000"

# -------------------------------
# API helpers
# -------------------------------
@st.cache_data
def get_all_players():
    """Fetches all player profiles from the API."""
    try:
        resp = requests.get(f"{API_BASE_URL}/profiles")
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching players: {e}")
        return []

@st.cache_data
def get_user_games(profile_id: int):
    """Fetches all games linked to a specific profile ID."""
    try:
        resp = requests.get(f"{API_BASE_URL}/profiles/{profile_id}/games")
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching games for user {profile_id}: {e}")
        return []

# -------------------------------
# Page title
# -------------------------------
st.title("🎮 Compare Players by Common Games")

# -------------------------------
# Fetch all players for selection
# -------------------------------
players = get_all_players()
if not players:
    st.info("Could not fetch players from the database.")
    st.stop()

# Create a dictionary for easy lookup of player details by username
player_map = {p['username']: p for p in players}

# -------------------------------
# Player selection
# -------------------------------
player1_name = st.selectbox("Select Player 1", list(player_map.keys()))
player2_name = st.selectbox("Select Player 2", list(player_map.keys()))

st.divider()

# -------------------------------
# Logic to find and select common games
# -------------------------------
if player1_name == player2_name:
    st.warning("Please select two different players.")
else:
    # Get the full profile objects for the selected players
    player1 = player_map[player1_name]
    player2 = player_map[player2_name]

    # Fetch the game lists for both players
    games1 = get_user_games(player1["profileID"])
    games2 = get_user_games(player2["profileID"])

    # Find the intersection of the two game lists
    games1_map = {g['gameID']: g['name'] for g in games1}
    games2_ids = {g['gameID'] for g in games2}

    common_game_ids = games1_map.keys() & games2_ids

    common_games = {gid: games1_map[gid] for gid in common_game_ids}

    if common_games:
        st.success("✅ Players have games in common! Please select one to compare.")

        # Create dropdown options from the common games
        game_options = {name: gid for gid, name in common_games.items()}
        selected_game_name = st.selectbox("Select Common Game", list(game_options.keys()))
        selected_game_id = game_options[selected_game_name]

        # Compare button
        if st.button("🔍 Compare Players", use_container_width=True, type="primary"):
            st.session_state["compare"] = {
                "player1_name": player1["username"],
                "player2_name": player2["username"],
                "game_id": selected_game_id,
                "game_name": selected_game_name,
                "show_maps_weapons": player1["isPremium"] and player2["isPremium"],
            }
            st.switch_page("pages/33_Compare_Players.py")
    else:
        st.info("❌ These two players don’t share any games in common.")
