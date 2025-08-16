import logging
import streamlit as st
import requests
from modules.nav import SideBarLinks

logger = logging.getLogger(__name__)

# -------------------------------
# Page setup
# -------------------------------
st.set_page_config(layout="wide")
SideBarLinks()

if "username" not in st.session_state or "profileID" not in st.session_state:
    st.error("Please log in to continue.")
    st.stop()

API_BASE_URL = "http://host.docker.internal:4000"  # Docker desktop host

# -------------------------------
# API helpers
# -------------------------------
@st.cache_data
def get_all_players():
    try:
        r = requests.get(f"{API_BASE_URL}/profiles")
        r.raise_for_status()
        return r.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching players: {e}")
        return []

@st.cache_data
def get_user_games(profile_id: int):
    try:
        r = requests.get(f"{API_BASE_URL}/profiles/{profile_id}/games")
        r.raise_for_status()
        return r.json()  # Expecting list of {"gameID": ...}
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching games: {e}")
        return []

# -------------------------------
# Page title
# -------------------------------
st.title("🎮 Compare Players by Common Games")

# -------------------------------
# Fetch all players
# -------------------------------
players = get_all_players()
if not players:
    st.info("No players available.")
    st.stop()

# -------------------------------
# Player selection
# -------------------------------
player1 = st.selectbox("Select Player 1", players, format_func=lambda p: p["username"])
player2 = st.selectbox("Select Player 2", players, format_func=lambda p: p["username"])

if player1["profileID"] == player2["profileID"]:
    st.warning("Please select two different players.")
else:
    # -------------------------------
    # Fetch games
    # -------------------------------
    games1 = get_user_games(player1["profileID"])
    games2 = get_user_games(player2["profileID"])

    # -------------------------------
    # Compute common games
    # -------------------------------
    games1_ids = {g["gameID"] for g in games1}
    games2_ids = {g["gameID"] for g in games2}

    common_ids = games1_ids & games2_ids

    if common_ids:
        # Map gameID -> display name (since API may not return name)
        common_games_map = {gid: f"Game {gid}" for gid in common_ids}

        # Selectbox showing only the display string
        selected_display_name = st.selectbox("Select Common Game", list(common_games_map.values()))

        # Reverse lookup to get the ID
        selected_game_id = next(gid for gid, display in common_games_map.items() if display == selected_display_name)

        # Compare button
        if st.button("🔍 Compare Players", use_container_width=True):
            st.session_state["compare"] = {
                "player1_name": player1["username"],
                "player2_name": player2["username"],
                "game_id": selected_game_id,
                "game_name": selected_display_name,
                "show_maps_weapons": player1["isPremium"] and player2["isPremium"],
            }
            st.switch_page("pages/33_Compare_Players.py")
    else:
        st.info("❌ These two players don’t share any games in common.")

# -------------------------------
# Back button
# -------------------------------
if st.button("⬅ Back to Home", use_container_width=True):
    st.switch_page("pages/05_Matthew_Bones_home.py")
