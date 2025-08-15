import streamlit as st
import requests
import logging
from modules.nav import SideBarLinks # Assuming this is your navigation module

# --- Configuration ---
st.set_page_config(layout="wide")
logger = logging.getLogger(__name__)
API_BASE_URL = "http://127.0.0.1:4000" # Replace with your actual Flask API URL

# --- Page Setup ---
SideBarLinks()

# Ensure user is logged in
if 'username' not in st.session_state or 'profileID' not in st.session_state:
    st.error("Please log in to add a new game.")
    st.stop()

profile_id = st.session_state['profileID']
username = st.session_state['username']

# --- Data Fetching Functions ---

@st.cache_data
def get_unlinked_games(profile_id):
    """
    Fetches all games and subtracts the ones already linked to the user's profile.
    """
    try:
        # 1. Fetch ALL games from the database
        response_all = requests.get(f"{API_BASE_URL}/games")
        response_all.raise_for_status()
        all_games = response_all.json()

        # 2. Fetch all games ALREADY linked to the user
        response_linked = requests.get(f"{API_BASE_URL}/games/profile/{profile_id}")
        response_linked.raise_for_status()
        linked_games = response_linked.json()

        # Create a set of linked game IDs for efficient lookup
        linked_game_ids = {game['gameID'] for game in linked_games}

        # 3. Filter the list in Python to find the difference
        available_games = [
            game for game in all_games if game['gameID'] not in linked_game_ids
        ]

        return available_games

    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching game lists: {e}")
        return []

def link_game_to_profile(profile_id, game_id, game_username):
    """
    Sends a request to link a selected game and username to the user's profile.
    This uses the POST endpoint you already created.
    """
    try:
        payload = {'gameID': game_id, 'profileID': profile_id, 'gameUsername': game_username}
        response = requests.post(f"{API_BASE_URL}/gameProfiles", json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

# --- UI Display ---

st.title("Link a New Game")
st.write("Add a new game to your profile to start tracking your stats.")
st.divider()

available_games = get_unlinked_games(profile_id)

if not available_games:
    st.success("You've added all available games to your profile!")
    st.balloons()
else:
    # Create a mapping from game name to gameID for the selectbox
    game_options = {game['name']: game['gameID'] for game in available_games}

    with st.form("link_game_form"):
        st.subheader("Select a Game")

        selected_game_name = st.selectbox(
            "Choose a game from the list:",
            options=game_options.keys()
        )

        game_username = st.text_input(
            "Enter your in-game username for this game:",
            placeholder="YourGamerTag#1234"
        )

        submitted = st.form_submit_button("Link Game to Profile", type="primary", use_container_width=True)

        if submitted:
            if not game_username:
                st.warning("Please enter your in-game username.")
            else:
                selected_game_id = game_options[selected_game_name]
                with st.spinner("Linking game..."):
                    result = link_game_to_profile(profile_id, selected_game_id, game_username)

                if "error" in result:
                    st.error(f"Failed to link game: {result['error']}")
                else:
                    st.success(f"Successfully linked **{selected_game_name}** to your profile!")
                    st.info("Your homepage will update with the new game shortly.")
                    # Clear the cache to force a refresh of the available games list
                    st.cache_data.clear()
