import streamlit as st
import requests
import logging
from modules.nav import SideBarLinks

# --- Configuration ---
st.set_page_config(layout='wide')
logger = logging.getLogger(__name__)
API_BASE_URL = "http://web-api:4000" # Replace with your API URL

# --- Page Setup ---
SideBarLinks()

# Ensure user is logged in
if 'username' not in st.session_state or 'profileID' not in st.session_state:
    st.error("Please log in to continue.")
    st.stop()

is_premium = st.session_state.get('is_premium', False)
username = st.session_state['username']
profile_id = st.session_state['profileID']

# --- Data Fetching Functions ---
@st.cache_data
def get_user_games(profile_id):
    """Fetches all games associated with a user's profile."""
    try:
        response_linked = requests.get(f"{API_BASE_URL}/games/profile/{profile_id}")
        response_linked.raise_for_status()
        linked_games = response_linked.json()
        return linked_games
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching games: {e}")
        return []

def unlink_game(profile_id, game_id):
    """Sends a DELETE request to unlink a game from the user's profile."""
    try:
        response = requests.delete(f"{API_BASE_URL}/games/profile/{profile_id}/{game_id}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error unlinking game: {e}")
        return None

# --- UI Display ---

# Title and welcome message
st.title(f"Welcome to Omni.gg, {username}.")
st.write('Your central hub for game analytics, player stats, and strategy tools.')
st.write('')

st.subheader("My Game Dashboards")
games_list = get_user_games(profile_id)

if games_list:
    # Use a session state variable to manage the confirmation dialog
    if 'confirming_removal' not in st.session_state:
        st.session_state.confirming_removal = None

    for game in games_list:
        game_name = game['name']
        game_id = game['gameID']

        col1, col2 = st.columns([4, 1]) # Make the first column wider

        with col1:
            if st.button(f"📊 View {game_name} Stats", key=f"view_{game_id}", use_container_width=True):
                st.session_state['selected_game_id'] = game_id
                st.session_state['selected_game_name'] = game_name
                st.session_state['viewing_profile_name'] = username
                st.switch_page("pages/31_View_Stats.py")

        with col2:
            if st.button("🗑️ Remove", key=f"remove_{game_id}", use_container_width=True):
                # When remove is clicked, store the game info for confirmation
                st.session_state.confirming_removal = {'id': game_id, 'name': game_name}
                st.rerun() # Rerun to show the confirmation dialog

else:
    st.info("You haven't added any games to your profile yet!")

# --- Confirmation Dialog Logic ---
if st.session_state.confirming_removal:
    game_to_remove = st.session_state.confirming_removal
    with st.container(border=True):
        st.warning(f"Are you sure you want to unlink **{game_to_remove['name']}** from your profile?")

        confirm_col1, confirm_col2 = st.columns(2)
        with confirm_col1:
            if st.button("Yes, unlink this game", key="confirm_yes", type="primary", use_container_width=True):
                unlink_game(profile_id, game_to_remove['id'])
                st.session_state.confirming_removal = None # Clear confirmation state
                st.cache_data.clear() # Clear cache to refresh game list
                st.success(f"{game_to_remove['name']} has been unlinked.")
                st.rerun()

        with confirm_col2:
            if st.button("No, cancel", key="confirm_no", use_container_width=True):
                st.session_state.confirming_removal = None # Clear confirmation state
                st.rerun()

# --- Page Links ---
if st.button("🔗 Link a New Game", use_container_width=True, type="secondary"):
    st.switch_page("pages/35_Link_Games.py")

st.divider()

# --- Other Navigation Buttons ---
st.subheader("Tools & Features")

if st.button('🤝 Compare Players', use_container_width=True):
    st.switch_page('pages/32_Select_Players.py')

if st.button(f"📜 View Match History",  use_container_width=True):
                st.switch_page("pages/match_history.py")
